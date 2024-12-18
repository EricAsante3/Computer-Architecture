from myhdl import block, always_comb, instances, intbv, Signal
from alu1 import ALU1bit

# tag: 1248-e7189dfac2e72068f319

# For large design, we can put blocks (hardware modules) in different Python
# modules 

#ALU1bit(a, b, carryin, binvert, operation, result, carryout):

@block
def ALU4bits(a, b, alu_operation, result, zero):

    """ 4-bit ALU

        See the diagram for details. 

    """
    # create internal signals in the 4-bit ALU

    # create bnegate and operation
    # We could create regular Signal objects. Then we need logic
    # to copy values from alu_operation to bnegate and operation.
    # So we create bnegate and operation as shadow signals.
    # They follow the bits in alu_operation 
    # If alu_operation changes, they change. 
    bnegate = alu_operation(2)      # bit 2 in alu_operation
    # like any range in Python, upper bound is open and lower is closed. 
    operation = alu_operation(2,0)  # bits 1 and 0 in alu_operation

    # Create signals for carryout of 1-bit ALUs.
    # In this lab, we use an individual variable for each signal.
    # TODO: create c2, c3, and c4
    c1 = Signal(bool(0))
    c2 = Signal(bool(0))
    c3 = Signal(bool(0))
    c4 = Signal(bool(0)) 

    # Create signals for result of 1-bit ALUs
    # We cannot use shadow signals from result because shadow
    # signals are read only. We will have to copy them to result manually
    # TODO: create result0, result1, result2, and result3
    result0 = Signal(bool(0))
    result1 = Signal(bool(0))
    result2 = Signal(bool(0))
    result3 = Signal(bool(0)) 


    # TODO
    # instantiate 1-bit ALUs
    # 
    # Use shadow signals to connnect individual bits in 
    # signals `a` and `b` to 1-bit ALUs. 
    # Use a(0) for bit 0 in signal a. Do NOT use a[0]. 
    # a(0) is a shadow signal that follows bit 0 in a
    # a[0] is bit 0's current value and it is not a Signal
    #ALU1bit(a, b, carryin, binvert, operation, result, carryout):

    alu1_0 = ALU1bit(a(0), b(0), bnegate, bnegate, operation, result0, c1)
    alu1_1 = ALU1bit(a(1), b(1), c1, bnegate, operation, result1, c2)
    alu1_2 = ALU1bit(a(2), b(2), c2, bnegate, operation, result2, c3)
    alu1_3 = ALU1bit(a(3), b(3), c3, bnegate, operation, result3, c4)


    @always_comb
    def comb_output():
        # TODO
        # Generate output signals `result` and `zero`
        # from the output of 1-bit ALUs, result0, result1, and so on
        #
        # There are 4 bits in `result`.
        # To set an individual bit in `result`, like bit 0, we do
        #   result.next[0] = ... 
        # To set bit 1 in `result`, we do
        #   result.next[1] = ... 
        # 
        # zero is generated with a NOR gate
        # use logical operators: and, or, not

    # do not change any lines below
    # return all logic
        result.next[0] = result0
        result.next[1] = result1
        result.next[2] = result2
        result.next[3] = result3
        zero.next =  (not (result.next[0] or result.next[1] or result.next[2] or result.next[3]))
    return instances()

if __name__ == "__main__":
    from myhdl import delay, instance, StopSimulation, bin
    import argparse

    N = 4

    # testbench itself is a block
    @block
    def test_comb(args):

        # create signals
        # use intbv for multiple bits
        a = Signal(intbv(0)[N:])
        b = Signal(intbv(0)[N:])
        result = Signal(intbv(0)[N:])
        alu_operation = Signal(intbv(0)[4:])
        zero = Signal(bool(0))

        # instantiating a block
        alu = ALU4bits(a, b, alu_operation, result, zero)

        @instance
        def stimulus():
            print("ALU_operation a     b    | result zero")
            UL = 1 << N
            for op in args.op:
                assert op in [0, 1, 2, 6]
                alu_operation.next = op
                for i in range(UL):
                    a.next = args.a
                    b.next = i
                    yield delay(10)
                    print("{:12}  {}  {} | {}   {}".format(
                        bin(op, 4), bin(a, N), bin(b, N),
                        bin(result, N), int(zero)))

            # stop simulation
            raise StopSimulation()

        return alu, stimulus

    operation_list = [0, 1, 2, 6]
    parser = argparse.ArgumentParser(description='4-bit ALU')
    parser.add_argument('op', nargs='*', type=int, default=operation_list, 
            help='list of alu operation in decimal.')

    parser.add_argument('-a', type=int, default=0b1010, help='input a in decimal')
    parser.add_argument('--trace', action='store_true', help='generate trace file')

    args = parser.parse_args()

    tb = test_comb(args)
    tb.config_sim(trace=args.trace)
    tb.run_sim()

