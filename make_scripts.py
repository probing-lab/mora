exit()

benchmarks = ["cc",
"cc4",
"random_walk_1d_cts",
"sum_rnd_series",
"product_dep_var",
"random_walk_2d",
"binomial",
"stutteringA",
"stutteringC",
"square",
"stutteringP",
"stutteringB",
"stutteringD",
"geometric"]

for b in benchmarks:
    for goal in [1, 2, 3]:
        with open(f"scripts/run_benchmark_{b}_{goal}.py","w+") as f:
            f.write("from mora.mora import mora\n")
            f.write(f'mora("benchmarks/{b}", goal={goal}, input_format="file", output_format="txt")')
