from mora.mora import mora

benchmarks = ["cc",
"sum_rnd_series",
"stutteringA",
"stutteringC",
"square"]

for b in benchmarks:
    for goal in [1, 2, 3]:
        mora("benchmarks/{}".format(b), goal=goal, input_format="file", output_format="eval")
