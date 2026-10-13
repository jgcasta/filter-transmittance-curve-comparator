# Transmission Curve Comparator

A browser-based tool for visualizing and combining spectral transmission curves from CSV files. Designed for astronomy and astrophotography workflows, including optical filters, telescope optics, and other wavelength-dependent transmission data.

## Features

- Import multiple CSV files using drag and drop or the file picker.
- Store imported curves locally in the browser using IndexedDB.
- Select multiple curves and display them together on an interactive XY chart.
- Rename and delete stored curves.
- Select all curves or clear the selection.
- Distinguish curves by color and display a legend.
- Automatically calculate and plot **Total Transmission** when two or more curves are selected.
- Run the application locally without a backend or database server.

![Screenshot](/images/screenshot1.png)

## Getting started

1. Download `filtros_con_transmitancia_total.html` from this repository.
2. Open the HTML file in a modern browser.
3. Drag CSV files onto the upload area, or click it to browse for files.
4. Select one or more curves from the list to display them.
5. Select at least two curves to see the combined transmission curve.

**Note:** The HTML file loads Chart.js from a CDN, so an internet connection is required to load the charting library unless you replace that dependency with a local copy. CSV storage and calculations take place locally.

## CSV format

Each file should contain two numeric columns:

1. **Wavelength** in nanometers (nm).
2. **Transmission** in percent, from **0 to 100**.

Example:

```csv
400,12
450,45
500,82
550,95
600,88
```

The CSV parser supports comma, semicolon, and tab separators and skips nonnumeric header rows. Data points are sorted by wavelength.

**Important:** Use percentages, not fractions: `80` means 80% transmission, whereas `0.8` is interpreted as 0.8%.

## Total transmission calculation

For multiple optical elements in series, the combined transmission at each wavelength is calculated by multiplying their fractional transmissions:

\[
T_{\mathrm{total}}(\lambda)
= 100\prod_{i=1}^{N}\frac{T_i(\lambda)}{100}
\]

Here, each input transmission \(T_i\) is expressed as a percentage between 0 and 100, and the result is also a percentage.

For example, two filters transmitting 80% and 90% at a given wavelength produce:

\[
T_{\mathrm{total}}=100\times0.80\times0.90=72\%
\]

### Different wavelength sampling

CSV files do not need to use identical wavelength points. The application:

1. Determines the wavelength range shared by all selected curves.
2. Creates a common wavelength grid from their available data points.
3. Uses linear interpolation to estimate each transmission at those wavelengths.
4. Multiplies the interpolated transmissions and plots the resulting curve.

The combined curve is limited to the overlapping wavelength range; values are not extrapolated beyond the available data.

## Data storage and privacy

Imported curves are saved in the browser's **IndexedDB** storage. They remain available between sessions as long as the browser retains that site's local data. They are not uploaded to a server.

Browser storage is specific to the browser and origin. Opening the file from a different browser, profile, or URL may show a different collection. Clearing browser data can remove stored curves.

## Technology

- HTML5 and CSS3
- Vanilla JavaScript
- IndexedDB for local persistence
- [Chart.js](https://www.chartjs.org/) for plotting

## Limitations

- The combined curve assumes independent multiplicative transmission through the selected elements.
- The application expects transmission percentages between 0 and 100.
- Linear interpolation is an approximation between measured CSV samples.
- This tool is intended for curve comparison and estimation, not as a substitute for calibrated spectrophotometric measurements.

## Suggested repository structure

```text
.
├── README.md
└── filtros_con_transmitancia_total.html
└── data
    └──curve1.csv
    └──curve2.csv
```

## License

No license has been specified. Add a `LICENSE` file if you want to define terms for reuse and redistribution.
