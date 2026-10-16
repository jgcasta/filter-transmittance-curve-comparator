# Transmission Curve Comparator

A local web application for viewing, managing, and combining spectral transmission curves from CSV files. It is designed for astronomy and astrophotography applications, such as comparing optical filters and estimating the combined transmission of an optical train.

https://jgcasta.github.io/filter-transmittance-curve-comparator/

## Features

- Automatically discovers and imports **all CSV files** in the `data/` directory (including subdirectories) when the page loads.
- Imports additional CSV files by drag and drop or file selection.
- Stores curves locally using **IndexedDB**, preserving them between browser sessions.
- Supports multiple selection, renaming, deletion, **Select all**, and **Clear selection**.
- Displays selected curves on an interactive wavelength-versus-transmission chart, with distinct colors and a legend.
- Calculates and plots the **total transmission** when two or more curves are selected.
- Uses linear interpolation to combine curves sampled at different wavelengths, over their common wavelength range.
- Runs on your own computer using a small Python HTTP server; no remote application backend is needed.

## Requirements

- Python 3 (standard library only).
- A modern browser with IndexedDB support.
- An internet connection to load **Chart.js from jsDelivr** in the current version. All CSV processing and storage remain local.

## Repository layout

```text
.
├── README.md
├── filtros_auto_data.html
├── servidor.py
└── data/
    ├── filter_OIII.csv
    ├── filter_Halpha.csv
    └── ...
```

The example CSV filenames are illustrative. Put your own files in `data/`; subdirectories are supported.

## Quick start

1. Clone or download the repository.
2. Copy your CSV files into the `data/` directory.
3. From the project directory, run:

   ```bash
   python3 servidor.py
   ```

4. Open **http://127.0.0.1:8765/filtros_auto_data.html** in your browser.

The server binds to `127.0.0.1` (localhost) on port `8765`. Refresh the page after adding or editing CSV files in `data/` to synchronize them. Stop the server with `Ctrl+C`.

> **Why a local server?** Browsers do not allow a standalone `file://` HTML page to enumerate files in a local directory automatically. `servidor.py` exposes a local `/api/data-files` endpoint that lists CSV files under `data/` and serves those files to the page.

## CSV format

Each CSV should contain two numerical columns:

1. Wavelength in **nanometers (nm)**.
2. Transmission in **percent (0–100)**.

Example:

```csv
Wavelength_nm,Transmission_percent
400,12
450,45
500,82
550,95
600,88
```

The parser accepts comma, semicolon, or tab delimiters, skips nonnumeric header rows, and sorts points by wavelength. Input transmission values must be percentages: **80 means 80%, not 0.80**.

## Total transmission

For optical components in series, the combined percentage transmission is:

$$
T_{\mathrm{total}}(\lambda) = 100\prod_{i=1}^{N}\frac{T_i(\lambda)}{100}
$$

Here, \(T_i(\lambda)\) is the percentage transmission of component \(i\) at wavelength \(\lambda\).

For example, if two filters transmit 80% and 90% at the same wavelength:

$$
T_{\mathrm{total}} = 100\times0.80\times0.90 = 72\%.
$$

When CSVs have different wavelength sampling, the application interpolates their values linearly onto a common set of wavelengths and calculates the product **only over the overlapping spectral range**. It does not extrapolate outside that range.

This multiplicative model is suitable for estimating the transmission of independent optical elements. It does not account for effects such as angle-dependent band shifts, multiple reflections, or detector quantum efficiency unless these are explicitly represented in the input curves.

## Automatic loading and local storage

On startup, the application asks the local server for the list of CSV files under `data/` and imports them into IndexedDB. Files previously imported from that directory are updated instead of duplicated, while their customized display names are preserved.

Manually imported CSVs also remain in IndexedDB. Renaming a curve changes its display name, not the original CSV filename. **Deleting a curve that is still present in `data/` does not permanently exclude it:** it will be imported again the next time the page loads. To remove it permanently, remove or move its source CSV from `data/` as well.

Browser storage is tied to the browser profile and origin; clearing site data may erase stored curves. CSV data is not sent to a remote server, although the Chart.js library is currently fetched from a public CDN.

## Technology

- HTML, CSS, and JavaScript
- [Chart.js](https://www.chartjs.org/)
- IndexedDB
- Python 3 standard-library HTTP server

## License

This project is licensed under the **Creative Commons Attribution–ShareAlike 4.0 International (CC BY-SA 4.0)** license.

You may share and adapt the material for any purpose, including commercially, provided that you:

- Give appropriate credit, provide a link to the license, and indicate if changes were made.
- Distribute adaptations under the same license.
- Do not impose additional legal or technological restrictions that prevent others from exercising the rights granted by the license.

See the [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/) for the full terms. For clarity in a GitHub repository, consider also adding a `LICENSE` file containing the official license text.

**Note:** Creative Commons generally recommends using software-specific licenses for source code. CC BY-SA 4.0 is stated here as the requested project license.
