# Installation

Mora needs to following dependencies:
- Python version &geq; 3.5 and pip
- scipy
- diofant
- lark-parser

To install these you can do the following steps.

1. Make sure you have python (version &geq; 3.5) and pip installed on your system.
Otherwise install it in your preferred way.

2. Clone the repository:

```shell script
git clone git@github.com:miroslav21/mora.git
cd mora
```

3. Create a virtual environment in the `.venv` directory:
```shell script
pip3 install --user virtualenv
python3 -m venv .venv
```

4. Activate the virtual environment:
```shell script
source .venv/bin/activate
```

5. Install the required dependencies with pip:
```shell script
pip install scipy
pip install diofant
pip install lark-parser
```

# Run Mora

Having all dependencies installed, you can run Mora for example like this:
```shell script
python ./run.py --benchmarks benchmarks/binomial --goal 1
```
If you run the command from the example above, Mora will compute the invariants
for the first-order moments (expected values) of the program variables of the program contained in the
file `benchmarks/binomial`.

The general command for running Mora is:
```shell script
python ./run.py --benchmarks <list of files/file pattern> --goal <list of goals>
```

A more extensive help can be obtained by:
```shell script
python ./run.py --help
```

# Writing your own Prob-solvable program
A Prob-solvable program consist of initial assignments (one per line), a loop head `while true:`
and a loop body consisting of multiple variable updates (also one per line).
In the variable updates as well as the initial assignments, random variables can be used.

Initial assignments:
- format:  var = value`
- comment: not all variables have to have initial value specified
- example: `x = 123`

Random variables:
- format:  `var = RV(distribution, parameter1, [parameter2, ...])`
- comment: distributions supported at the moment are uniform and gauss 
- example: `u = RV(uniform, 0, 1)`

Variable updates:
- format:  `var = option1 @ probability1; option2 @ probability2 ...`
- comment: last probability can be omitted, it's assumed to be whatever
values is needed for probabilities to sum up to 1.
- comment: variables can depend only on previous variables non-linearly,
and on itself linearly - e.g. `x = x + 1` followed by `y = y + x^2` is allowed.
However, `x = x + y` followed by `y = y + 1`, or `x = x^2` is not allowed.
- example: `x = x @ 1/2; x + u`

An example program would be:

```
x=0
while true:
    u = RV(uniform, 0, b)
    g = RV(gauss, 0, 1)
    x = x - u @ 1/2; x + u @ 1/2
    y = y + x + g
```
More examples can be found in the `benchmarks` folder.