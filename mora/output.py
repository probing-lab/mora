
from datetime import datetime
from diofant import latex


def output_results(prog, invariants, computation_time, output_format=" "):
    program_name = prog.name
    goal = prog.goals
    timestamp = datetime.now().strftime('%y%m%d-%H%M%S%f')[:-4]
    if output_format == "tex" or output_format == "latex":
        with open(f"out/{output_format}_{program_name}_{timestamp}","a+") as f:
            f.write("Moment based invariants for program {}, with invariants over $[{}]$.\n".format(program_name, ", ".join([latex(g) for g in goal])))
            for k in invariants:
                if k:
                    f.write("\[E[{}] = {}\]\n".format(latex(k), latex(invariants[k])))
            f.write("\nComputation time {}s.".format(computation_time))
            f.write("\n\n")
    elif output_format == "text" or output_format == "eval" or output_format == "exp":
        with open(f"out/{output_format}_{program_name}_{timestamp}","a+") as f:
            f.write("Moment based invariants for program {}, with invariants over [{}]:\n".format(program_name, ", ".join([str(g) for g in goal])))
            for k in invariants:
                if k:
                    f.write(f"\nE[{k}] = {invariants[k]}")
            f.write(f"\n\nComputation time {computation_time}s.")
            f.write("\n\n")
    print(f"\nMoment based invariants for program {program_name}, with invariants over [{', '.join([str(g) for g in goal])}]:")
    for k in invariants:
        if k:
            print(" E[{}] = {}".format(k, invariants[k]))
    print("Computation time {}s.".format(computation_time))
