import pandas as pd
from toc_connect.core import fisher_z_connectivity


def test_fisher_z_matrix_has_zero_diagonal_and_labels():
    frame = pd.DataFrame({"OFC": [1, 2, 3, 4], "caudado": [4, 3, 2, 1]})
    result = fisher_z_connectivity(frame)
    assert list(result.columns) == ["OFC", "caudado"]
    assert result.loc["OFC", "OFC"] == 0
    assert result.loc["OFC", "caudado"] < 0
