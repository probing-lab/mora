
from datetime import datetime
from diofant import latex


def output_results(prog, invariants, computation_time, output_format=" "):
    program_name = prog.name
    timestamp = datetime.now().strftime('%y%m%d-%H%M%S%f')[:-4]
    if output_format == "tex" or output_format == "latex":
        with open(f"out/{output_format}_{program_name}_{timestamp}","a+") as f:
            for k in invariants:
                if k:
                    f.write("\[E[{}] = {}\]\n".format(latex(k.as_expr()), latex(invariants[k])))
            f.write("\nComputation time {}s.".format(computation_time))
            f.write("\n\n")
    elif output_format == "text" or output_format == "eval" or output_format == "exp":
        with open(f"out/{output_format}_{program_name}_{timestamp}","a+") as f:
            for k in invariants:
                if k:
                    f.write(f"\nE[{k.as_expr()}] = {invariants[k]}")
            f.write(f"\n\nComputation time {computation_time}s.")
            f.write("\n\n")
    for k in invariants:
        if k:
            print(" E[{}] = {}".format(k.as_expr(), invariants[k]))
    print("Computation time {}s.".format(computation_time))
    return [" E[{}] = {}".format(k.as_expr(), invariants[k]) for k in invariants if k]
