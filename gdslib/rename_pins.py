def rename_pins(circuit, pins):
    """FIXME! and add test
    """
    for k, new_pin_name in pins.items():
        element, pin = k
        print(element, pin, new_pin_name)
        circuit.elements[element].pins[pin] = new_pin_name


if __name__ == "__main__":
    import pp
    import gdslib as gl

    c = pp.c.mzi(DL=100)
    cm = gl.circuit(c)

    cm = rename_pins(
        cm, {("mmi1x2_12_0", "W0"): "input", ("mmi1x2_98_0", "W0"): "output"},
    )
    gl.plot_circuit(cm)
