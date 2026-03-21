import math

from app.config import GPU_NODE, HOSTNAME


async def calculate_ml_score(x: float) -> dict:

    outer_iterations = 90 if GPU_NODE else 180
    inner_iterations = 45_000

    base = abs(x) + 1.0

    total_1 = 0.0
    total_2 = 0.0
    total_3 = 0.0
    total_4 = 0.0

    for outer in range(1, outer_iterations + 1):
        outer_f = float(outer)

        acc1 = 0.0
        acc2 = 0.0
        acc3 = 0.0

        shift = base * outer_f * 0.0137

        for i in range(1, inner_iterations + 1):
            fi = float(i)

            sqrt_i = math.sqrt(fi)
            log_i = math.log(fi + 1.0)
            inv1 = 1.0 / (fi ** 1.07)
            inv2 = 1.0 / (fi ** 1.11)
            inv3 = 1.0 / (fi ** 1.15)

            s1 = math.sin(x / (sqrt_i + 1.0) + log_i * 0.7 + outer_f)
            c1 = math.cos(x * 0.00021 * fi + shift / (sqrt_i + 1.0))
            s2 = math.sin((base + log_i) / (fi ** 0.23) + outer_f * 0.17)
            c2 = math.cos((x + fi * 0.0003) * 0.11 + log_i / (outer_f + 1.0))

            mix1 = s1 * c1
            mix2 = s2 + c2
            mix3 = (s1 + s2) * (c1 - c2)

            acc1 += mix1 * inv1
            acc2 += mix2 * inv2
            acc3 += mix3 * inv3

        block = (
            math.tanh(acc1 * 2.7)
            + math.sin(acc2 * 3.1)
            + math.cos(acc3 * 2.3)
            + math.sin((acc1 + acc2) * 1.9)
            + math.cos((acc2 + acc3) * 1.4)
        )

        total_1 += block / (outer_f ** 0.5)
        total_2 += (acc1 * acc2) / (outer_f ** 1.2)
        total_3 += (acc2 - acc3) / (outer_f ** 0.9)
        total_4 += math.sin(block + acc1 + acc3) / outer_f

    final_raw = (
        math.tanh(total_1)
        + math.sin(total_2 * 0.0008)
        + math.cos(total_3 * 0.015)
        + math.tanh(total_4 * 1.7)
        + math.sin((total_1 + total_2 + total_3 + total_4) * 0.002)
    )

    score = round((math.tanh(final_raw) + 1) * 50, 3)

    return {
        "backend_hostname": HOSTNAME,
        "score": score,
        "gpu_node": GPU_NODE,
        "explanation": (
            "Сейчас score вычисляется через тяжелую CPU-bound детерминированную "
            "математику в ml-service, чтобы наглядно показать выигрыш от кэширования."
        ),
    }