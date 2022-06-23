import math

V = 1.0
D = 0.1
L = 10.0
T = 5.0


def get_x_set(pe):
    # step on x
    h = pe * D / V
    # amount of steps on x
    n1 = int((L / h) + 1)

    x = [0]

    for i in range(1, n1+1):
        x.append((i-1) * h)

    x.pop(0)
    return x


def calculate_exact(pe):
    # step on x
    h = pe * D / V
    # amount of steps on x
    n1 = int((L / h) + 1)
    # result array
    u = [0]*(n1 + 1)

    math.erfc(0.67)

    for i in range(1, n1+1):
        x = (i-1) * h
        u[i] = 0.5 * (math.erfc((x - V * T) / (2 * math.sqrt(D * T))) +
                    math.exp((V * x) / D) * math.erfc((x + V * T) / (2 * math.sqrt(D * T))))
    u.pop(0)
    return u


def classic_scheme(cu, pe):
    # step on x
    h = pe * D / V
    # step on t
    tau = cu * h / V

    # amount of steps on x
    n1 = int((L / h) + 1)
    # amount of steps on t
    n2 = int((T / tau) + 1)

    # equation coefficients
    A = [0]*(n1 + 1)
    B = [0]*(n1 + 1)
    C = [0]*(n1 + 1)
    F = [0]*(n1 + 1)

    # the result vector
    u = [0]*(n1 + 1)

    a = D / (h * h) + V / (2 * h)
    b = D / (h * h) - V / (2 * h)
    c = a + b + 1 / tau

    # filling up matrix and vector of right sides
    C[1] = 1
    F[1] = 1
    C[n1] = 1

    for i in range(2, n1):
        A[i] = a
        B[i] = b
        C[i] = c

    # helping arrays of alphas and betas
    alpha = [0]*(n1 + 1)
    beta = [0]*(n1 + 1)

    for j in range(1, n2+2):
        # right stroke
        alpha[1] = B[1] / C[1]
        beta[1] = F[1] / C[1]

        for i in range(2, n1):
            denominator = C[i] - A[i] * alpha[i - 1]
            alpha[i] = B[i] / denominator
            beta[i] = (F[i] + A[i] * beta[i - 1]) / denominator

        # back stroke
        u[n1] = (F[n1] + A[n1] * beta[n1 - 1]) / (C[n1] - A[n1] * alpha[n1 - 1])
        for i in range(n1-1, 0, -1):
            u[i] = alpha[i] * u[i + 1] + beta[i]
            F[i] = u[i]/tau

        F[1] = 1

    u.pop(0)
    return u


def characteristics_scheme(cu, pe):
    # step on x
    h = pe * D / V
    # step on t
    tau = cu * h / V

    # amount of steps on x
    n1 = int((L / h) + 1)
    # amount of steps on t
    n2 = int((T / tau) + 1)

    # equation coefficients
    A = [0]*(n1 + 1)
    B = [0]*(n1 + 1)
    C = [0]*(n1 + 1)
    F = [0]*(n1 + 1)

    # the result vector
    u = [0]*(n1 + 1)

    ab = D / (h * h)
    c = 2 * ab + 1 / tau

    # filling up matrix and vector of right sides
    C[1] = 1
    F[1] = 1
    C[n1] = 1

    for i in range(2, n1):
        A[i] = ab
        B[i] = ab
        C[i] = c

    # helping arrays of alphas and betas
    alpha = [0]*(n1 + 1)
    beta = [0]*(n1 + 1)

    for j in range(1, n2 + 2):
        # right stroke
        alpha[1] = B[1] / C[1]
        beta[1] = F[1] / C[1]

        for i in range(2, n1):
            denominator = C[i] - A[i] * alpha[i - 1]
            alpha[i] = B[i] / denominator
            beta[i] = (F[i] + A[i] * beta[i - 1]) / denominator

        # back stroke
        u[n1] = (F[n1] + A[n1] * beta[n1 - 1]) / (C[n1] - A[n1] * alpha[n1 - 1])
        for i in range(n1 - 1, 0, -1):
            u[i] = alpha[i] * u[i + 1] + beta[i]
            F[i] = u[i] / tau

        for i in range(n1 - 1, 1, -1):
            F[i] = interpolate(u, cu, i)/tau

        F[1] = 1

    u.pop(0)
    return u


def interpolate(u, cu, i):
    m = math.floor(cu)
    alpha = cu - m

    if i-m < 0:
        return 1
    elif i-m-1 < 0:
        return 1
    else:
        return alpha * u[i-m-1] + (1-alpha)*u[i-m]
