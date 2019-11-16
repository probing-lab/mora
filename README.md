# Installation

To install dependencies and set up Mora:
1. Open terminal in in the main 'mora/' folder. 
2. Run "./setup_off".
This process may take up to several minutes. No internet connection is assumed, and there may be some warnings/errors due to redundant installations of dependencies. Please ignore those.


# Rerun Experiments

To rerun experiments from the paper:
1. Open terminal in in the main 'mora/' folder.
2a. Run "python3.7 scripts/run_evaluation.py" to rerun Mora on subset of benchmarks shown in the tool demonstration paper submission.
2b. Run "python3.7 scripts/run_experiments.py" to rerun Mora on the entire set of benchmarks.
Even on VM, running Mora on all benchmarks should not take more than 5-10 minutes.
The results are shown in the terminal as they are computed, and also output in the "out/" folder. Results for each run are stored in separate file called "eval_NAME_TIMESTAMP" for run_evaluation, and "exp_NAME_TIMESTAMP" for run_experiments. For easier viewing, you can concatenate output from all the runs to a single text file 'output_evaluation', 'output_experiments', respectively,  with:
3a. "cat out/eval_* > output_evaluation" 
3b. "cat out/exp_* > output_experiments"
4. You can run any single of the benchmarks using scripts in '/script' folder, e.g. "python3.7 scripts/run_benchmark_stutteringA_2.py" for 'stutteringA' program with goal '2'. Output will be stored as 'txt_NAME_TIMESTAMP' in the 'out' folder.


# Run on own programs

The easiest way to run Mora on your own program is to create a file containing the program. The program should follow format as described in the paper. TL;DR version below, also check programs in 'benchmarks' folder for examples. 

1. Open terminal in in the main 'mora/' folder.
2. Run "python3.7" command.
3. Run "from mora.mora import mora".
4. You can run mora by running following: "mora(INPUT, GOAL, input_format=INPUT_FORMAT, output_format=OUTPUT_FORMAT)",
where:
INPUT: either path to your program (if input_format="file" - default option), or your program as a string (if input_format="string"). If program from a file is used, path should can be absolute, or relative w.r.t. the main 'mora' folder. 
GOAL: A goal (or list of goals) as a string (or list of strings). Each goal can be either a specific moment, or a number, say k, (in which case k-th moments of all variables are considered as goals). 
INPUT_FORMAT: unspecified, "file", or "strings", as described above.
OUTPUT_FORMAT: By default the results are output to the screen after computation, but may be specified to "tex" or "txt", in which case an output file is created in 'out' folder. "txt" format saves the results in a text file in a simple, readable format, while "tex" output can be inserted directly to a latex document.
Outputfiles are saved as "FORMAT_PROGRAM_TIMESTAMP", where FORMAT is either "txt" or "tex", PROGRAM is name of the program file, or "string_input", and TIMESTAMP is time of output to distinguish between consecutive runs on the same program.

For example, one can run "mora('benchmarks/stutteringA', goal=[1, 'x^2', 'x^3'])" to compute expected values of all variables and second and third moments of 'x' in program 'stutteringA' and output to screen.


# TL;DR Program model
Program consist of initial assignments (one per line), loop line "while true:", random variables, and variable updates (one line per variable). 

Initial assignments:
    - format:  var = value
    - comment: not all variables have to have initial value specified
    - example: x = 123

Random variables:
    - format:  var = RV(distribution, parameter1, [parameter2, ...])
    - comment: distributions supported at the moment are uniform and gauss 
    - example: u = RV(uniform, 0, 1)

Variable updates:
    - format:  var = option1 @ probability1; option2 @ probability2 ...
    - comment: last probability can be omitted, it's assumed to be whatever values is needed for probabilities to sum up to 1.
    - comment: variables can depend only on previous variables non-linearly, and on itself linearly - e.g. (x = x + 1 followed by y = y + x^2) is allowed but (x = x + y followed by y = y + 1), or (x = x^2) are not.
    - example: x = x @ 1/2; x + u

An example program would be:

```
x=0
while true:
    u = RV(uniform, 0, b)
    g = RV(gauss, 0, 1)
    x = x - u @ 1/2; x + u @ 1/2
    y = y + x + g
```


















