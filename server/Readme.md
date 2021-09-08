# Currency Converter Service

This skeleton provides an implementation of a REST service to perform currency conversions.
You need to add the business logic for the conversion to work. These are the specs:

- The service must convert an amount from any currency to any other currency.
- You can find the definition and usage of the endpoint at http://localhost:900/ or `main.py`.
- The data used for the conversion can be obtained from the `utils.get_currencies` function.
- Try to make your code as **clear** and **efficient** as possible.

## Task

- The required parameters should be called `from`,`to` & `amount`.
- There should be an optional parameter called `precision` which should have a default vale of `4`.
- The `precision` parameter describes the precision of the return value. For e.g. `precision=4` returns `1.0000` and if `precision=6` returns `1.000000`
- Only currencies in the [link](https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml) should be accepted.
- Use the `convert` route for implementation.

## Acceptance criteria

- All tests must pass. you can run tests by running `python3 -m pytest` in the terminal in this directory.
- Parameters must be integers and currency codes must conform to ISO-4217 (3 letters, uppercase).
- Make sure errors are handled properly (correct return codes & messages).
