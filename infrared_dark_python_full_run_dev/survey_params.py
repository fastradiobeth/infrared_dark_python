# survey_params.py
# ***************************************************************************
# because people should at least be given the option to use something
# that isn't Hi-GAL
# ***************************************************************************
# INFRARED DARK PYTHON
# September 2015
# Beth Jones
# School of Physics and Astronomy | University of Manchester
# ***************************************************************************
"""
Beam widths [arcsec] for use with infrared_dark_python specific to
telescope survey seleted. Currently contains surveys:
	0 - Herschel 60"/s (Hi-GAL)

Additional surveys can be added to this file, and other survey-specific
parameter categories as required.
"""
higal_beams = {
	70: 10.2,
	160: 13.55,
	250: 18.0,
	350: 24.0,
	500: 34.5
}

surveys = {
    0: higal_beams
}
