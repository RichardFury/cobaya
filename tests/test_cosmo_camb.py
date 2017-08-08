# Tries to evaluate the likelihood at LCDM's best fit of Planck 2015, with CAMB

from cobaya.conventions import input_theory, input_likelihood, input_sampler
from cobaya.conventions import input_params, _chi2, separator, input_path_install
from cobaya.yaml_custom import yaml_custom_load
from cobaya.run import run

from cosmo_common import params_lowl_highTT, chi2_lowl_highTT
from cosmo_common import params_lowTEB_highTTTEEE, chi2_lowTEB_highTTTEEE
from cosmo_common import derived, tolerance_abs

def test_camb_planck_t(modules):
    body_of_test(modules, "t")
    
def test_camb_planck_p(modules):
    body_of_test(modules, "p")

def body_of_test(modules, x):
    assert modules, "I need a modules folder!"
    info = {input_path_install: modules,
            input_theory: {"camb": None},
            input_sampler: {"evaluate": None}}
    if x == "t":
        info[input_likelihood] = {"planck_2015_lowl": None,
                                  "planck_2015_plikHM_TT": None}
        info.update(yaml_custom_load(params_lowl_highTT))
        ref_chi2 = chi2_lowl_highTT
    elif x == "p":
        info[input_likelihood] = {"planck_2015_lowTEB": None,
                                  "planck_2015_plikHM_TTTEEE": None}
        info.update(yaml_custom_load(params_lowTEB_highTTTEEE))
        ref_chi2 = chi2_lowTEB_highTTTEEE
    else:
        raise ValueError("Test not recognised: %r"%x)
    # Remove H0 in favour of cosmomc_theta
    info[input_params][input_theory].pop("H0")
    # Add derived
    info[input_params][input_theory].update(derived)
    updated_info, products = run(info)
    # print products["sample"]
    # Check value of likelihoods
    for lik in info[input_likelihood]:
        chi2 = products["sample"][_chi2+separator+lik][0]
        assert abs(chi2-ref_chi2[lik]) < tolerance_abs, (
            "Likelihood value for '%s' off by more than %f!"%(lik, tolerance_abs))
    # Check value of derived parameters
    ###################
    ###################
    ###################
