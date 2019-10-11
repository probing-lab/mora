from mora import mora

benchmarks = ["cc",
"cc4",
"random_walk_1d_cts",
"sum_rnd_series",
"product_dep_var",
"random_walk_2d",
"binomial",
"introA",
"introC",
"square",
"introP",
"test_init_rv",
"introB",
"introD",
"geometric"]

for b in benchmarks:
    for goal in [1, 2, 3]:
        mora("benchmarks/{}".format(b), goal=goal, input_format="file", output_format="txt")
