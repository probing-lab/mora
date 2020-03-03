from mora.input import InputParser
import termination.structure_store as structure_store
import termination.bound_store as bound_store


def bounds(benchmark, expression):
    ip = InputParser()
    ip.set_source(benchmark)
    program = ip.parse_source()
    structure_store.set_program(program)
    bound_store.set_program(program)
    st = bound_store.get_bounds_of_expr(expression)
    print("Expression: ", st.expression.as_expr())
    print("Lower bound: ", st.lower)
    print("Upper bound: ", st.upper)
    print("Maybe positive: ", st.maybe_positive)
    print("Maybe negative: ", st.maybe_negative)
