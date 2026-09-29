import os
import sys
import subprocess
import yaml
import duckdb

ONTO_PATH = os.path.join(os.path.dirname(__file__), "..", "ontology", "ontology.yaml")
ONTO = yaml.safe_load(open(ONTO_PATH))

def test_every_property_maps_to_a_real_column():
    db_path = os.path.join(os.path.dirname(__file__), "..", "retail.duckdb")
    con = duckdb.connect(db_path, read_only=True)
    cols = set(con.execute("select table_name, column_name from information_schema.columns").fetchall())
    missing = []
    for obj_name, obj in ONTO["object_types"].items():
        for prop_name, p in obj["properties"].items():
            parts = p["maps_to"].split(".")
            if len(parts) == 2:
                tbl, col = parts
                if (tbl, col) not in cols:
                    missing.append(p["maps_to"])
    assert not missing, f"Ontology references missing columns: {missing}"

def test_every_definition_metric_exists_in_semantic_layer():
    mf_cmd = os.path.join(os.path.dirname(__file__), "..", ".venv", "Scripts", "mf.exe")
    if not os.path.exists(mf_cmd):
        mf_cmd = "mf"
    
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env["PYTHONIOENCODING"] = "utf-8"
    
    res = subprocess.run(
        [mf_cmd, "list", "metrics"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        cwd=os.path.join(os.path.dirname(__file__), "..")
    )
    out = res.stdout + res.stderr
    
    expected_metrics = [ONTO["definitions"]["ActiveCustomer"]["metric"]] + \
                       [v["metric"] for v in ONTO["definitions"]["ActiveCustomer"]["variants"]]
    
    missing = [m for m in expected_metrics if m not in out]
    assert not missing, f"Missing metrics in semantic layer: {missing}. Command output:\n{out}"
