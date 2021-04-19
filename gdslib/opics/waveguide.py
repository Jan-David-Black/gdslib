from opics.libraries.ebeam import Waveguide


def straight(width=0.5, length=10, height=0.22, dB_per_cm=3.0, **kwargs):
    """Waveguide model from opics."""
    return Waveguide(
        width=width * 1e-6, wg_length=length * 1e-6, height=height, TE_loss=dB_per_cm
    )


if __name__ == "__main__":
    c = straight()
