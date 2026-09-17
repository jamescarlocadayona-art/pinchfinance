# Pinch Finance 0.1 beta

## Portable use

Run `PinchFinance.exe` directly. The app stores its database in:

`%LOCALAPPDATA%\PinchFinance\pinch_finance.db`

## Install shortcuts

Put `PinchFinance.exe` and `install_pinch_finance.ps1` in the same folder. Right-click `install_pinch_finance.ps1`, choose **Run with PowerShell**, and confirm the Windows prompt if shown.

The installer creates:

- `%LOCALAPPDATA%\Programs\PinchFinance\PinchFinance.exe`
- A Start Menu shortcut
- A Desktop shortcut

No administrator access is required.

## Upload

For sharing, upload `PinchFinance.exe` and `install_pinch_finance.ps1` together, or upload the ZIP package. Do not upload `pinch_finance.db` unless you intentionally want to share the local finance data.

Windows may show a SmartScreen warning because this beta executable is not digitally signed.
