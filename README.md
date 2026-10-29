# zero_bias

Analysis code for the paper:

> **Unclustered tracers remain unclustered: the lack of primordial non-Gaussianity response of bias-zero tracers**
> C. Merino, S. Avila, A. G. Adame, A. Anguren, V. Gonzalez-Perez, J. Meneses-Rizo
> *Astronomy & Astrophysics*, 707, L15 (2026).
> [doi:10.1051/0004-6361/202558825](https://doi.org/10.1051/0004-6361/202558825) · [arXiv:2602.04698](https://arxiv.org/abs/2602.04698)

The paper tests whether unclustered tracers (linear bias $b_1 = 0$), selected by their local density, can be used
to constrain local primordial non-Gaussianity (PNG). Using the PNG-UNITsim simulations, we classify halos by their
local overdensity, measure their power spectra, and fit the linear bias $b_1$ and the PNG response $b_\phi f_{\rm NL}$.
We find $b_\phi \approx 0$ for all bias-zero tracers considered.

## Contents

| File | Description |
|------|-------------|
| `delta_compute.py` | Computes the local halo overdensity $\delta_{h,R}$ of each halo, counting its neighbours within a sphere of radius $R = 8\,h^{-1}$Mpc (periodic KD-tree). |
| `df_eval.py` | Evaluates the smoothed dark matter density field $\delta_{m,R}$ at the position of each halo (used for the classification by matter overdensity). |
| `power_spectra.ipynb` | Splits the halos into equally populated $\delta$ bins and computes, for each bin, the halo auto-power spectrum $P_{hh}$, the matter power spectrum $P_{mm}$ and the halo–matter cross-power spectrum $P_{hm}$. |
| `emcee.ipynb` | MCMC fits of $b_1$ and $b_\phi f_{\rm NL}$ (plus a shot-noise term for the auto-spectra) to the power spectra of each bin, using the scale-dependent bias model. |

## Workflow

1. Run `delta_compute.py` on a halo catalogue to get the local overdensity of each halo
   (or `df_eval.py` to classify by the dark matter overdensity instead).
2. Run `power_spectra.ipynb` to bin the halos in $\delta$ and compute the auto-, matter and cross-power spectra.
3. Run `emcee.ipynb` to fit $b_1$ and $b_\phi f_{\rm NL}$ for each bin, first with the auto-spectra and then with the cross-spectra.

All input and output paths are placeholders (`/path/to/...`) and need to be set before running.

## Requirements

- Python 3 with `numpy`, `scipy`, `pandas` and `matplotlib`
- [`nbodykit`](https://nbodykit.readthedocs.io/) (power spectra)
- [`Pylians`](https://pylians3.readthedocs.io/) (`MAS_library`, `smoothing_library`; only for `df_eval.py`)
- [`emcee`](https://emcee.readthedocs.io/), [`camb`](https://camb.readthedocs.io/) and [`getdist`](https://getdist.readthedocs.io/) (fits)

## Data

The PNG-UNITsim and UNIT simulations used in the paper are publicly available at
[unitsims.org](http://www.unitsims.org/) and [PIC Open Data](https://opendata.pic.es/unitsims).
The scripts expect the `z = 1` Rockstar halo catalogues in HDF5 format.

## Credits

The MCMC fitting code in `emcee.ipynb` was originally provided by A. G. Adame, with modifications
to include the shot-noise amplitude as a free parameter.

## Citation

If you use this code, please cite the paper:

```bibtex
@article{Merino2026,
  author  = {Merino, C. and Avila, S. and Adame, A. G. and Anguren, A. and Gonzalez-Perez, V. and Meneses-Rizo, J.},
  title   = {Unclustered tracers remain unclustered: the lack of primordial non-Gaussianity response of bias-zero tracers},
  journal = {Astronomy \& Astrophysics},
  volume  = {707},
  pages   = {L15},
  year    = {2026},
  doi     = {10.1051/0004-6361/202558825},
  eprint  = {2602.04698},
  archivePrefix = {arXiv}
}
```

## License

MIT, see [LICENSE](LICENSE).
