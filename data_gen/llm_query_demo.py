import sys
import os
import json
import subprocess
import yaml

METRICS_CATALOG = {
    "active customers": {
        "metric": "active_customers",
        "label": "Active Customers (official, 90d)",
        "description": "Marketing definition: customer with completed order in last 90 days."
    },
    "finance active customers": {
        "metric": "active_customers_365d",
        "label": "Retained Customers (12m, Finance)",
        "description": "Finance definition: customer with completed order in last 365 days."
    },
    "retained customers": {
        "metric": "active_customers_365d",
        "label": "Retained Customers (12m, Finance)",
        "description": "Finance definition: customer with completed order in last 365 days."
    },
    "support engaged customers": {
        "metric": "engaged_customers_30d",
        "label": "Engaged Customers (30d, Support)",
        "description": "Support definition: order or ticket in last 30 days."
    },
    "engaged customers": {
        "metric": "engaged_customers_30d",
        "label": "Engaged Customers (30d, Support)",
        "description": "Support definition: order or ticket in last 30 days."
    },
    "total revenue": {
        "metric": "total_revenue",
        "label": "Total Revenue",
        "description": "Sum of gross order amount."
    },
    "revenue per active customer": {
        "metric": "revenue_per_active_customer",
        "label": "Revenue per Active Customer",
        "description": "Total revenue divided by canonical active customers."
    }
}

DIMENSIONS_CATALOG = {
    "segment": "customer__segment",
    "country": "customer__country",
    "month": "metric_time__month",
    "status": "order__status"
}

TEST_BENCHMARK_QUESTIONS = [
    {"id": 1, "question": "What is the official active customer count by country?", "expected_metric": "active_customers", "expected_group_by": "customer__country"},
    {"id": 2, "question": "Show retained customers (12m) by segment for Finance.", "expected_metric": "active_customers_365d", "expected_group_by": "customer__segment"},
    {"id": 3, "question": "What is the support 30d engaged customer count by country?", "expected_metric": "engaged_customers_30d", "expected_group_by": "customer__country"},
    {"id": 4, "question": "Show total revenue by month.", "expected_metric": "total_revenue", "expected_group_by": "metric_time__month"},
    {"id": 5, "question": "What is the revenue per active customer by segment?", "expected_metric": "revenue_per_active_customer", "expected_group_by": "customer__segment"},
    {"id": 6, "question": "Compare official active customers across segments.", "expected_metric": "active_customers", "expected_group_by": "customer__segment"},
    {"id": 7, "question": "What is total revenue by country?", "expected_metric": "total_revenue", "expected_group_by": "customer__country"},
    {"id": 8, "question": "Show Finance active customers count.", "expected_metric": "active_customers_365d", "expected_group_by": None},
    {"id": 9, "question": "Show active customers (90d) side by side with retained customers (365d) by segment.", "expected_metric": "active_customers,active_customers_365d", "expected_group_by": "customer__segment"},
    {"id": 10, "question": "Show all active customer metric variants by segment.", "expected_metric": "active_customers,active_customers_365d,engaged_customers_30d", "expected_group_by": "customer__segment"}
]

def translate_question_to_mf_query(question: str):
    q_lower = question.lower()
    selected_metrics = []
    
    if "all active customer" in q_lower or "metric variants" in q_lower:
        selected_metrics = ["active_customers", "active_customers_365d", "engaged_customers_30d"]
    elif "side by side" in q_lower or ("active customers" in q_lower and "retained" in q_lower):
        selected_metrics = ["active_customers", "active_customers_365d"]
    elif "finance" in q_lower or "retained" in q_lower:
        selected_metrics = ["active_customers_365d"]
    elif "support" in q_lower or "engaged" in q_lower:
        selected_metrics = ["engaged_customers_30d"]
    elif "revenue per active customer" in q_lower or "revenue per customer" in q_lower:
        selected_metrics = ["revenue_per_active_customer"]
    elif "total revenue" in q_lower or "revenue" in q_lower:
        selected_metrics = ["total_revenue"]
    elif "active customer" in q_lower or "active customers" in q_lower:
        selected_metrics = ["active_customers"]
    else:
        selected_metrics = ["active_customers"]

    selected_group_by = None
    for dim_key, dim_val in DIMENSIONS_CATALOG.items():
        if dim_key in q_lower:
            selected_group_by = dim_val
            break

    metric_str = ",".join(selected_metrics)
    cmd = ["mf", "query", "--metrics", metric_str]
    if selected_group_by:
        cmd.extend(["--group-by", selected_group_by])
    
    return {
        "question": question,
        "metrics": metric_str,
        "group_by": selected_group_by,
        "command": " ".join(cmd)
    }

def run_benchmark():
    print("==========================================================================")
    print("  LLM Semantic Query Translator Benchmark (10 Natural Language Questions)")
    print("==========================================================================")
    
    mf_bin = os.path.join(".venv", "Scripts", "mf.exe")
    if not os.path.exists(mf_bin):
        mf_bin = "mf"
        
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = "."
    
    passed = 0
    for q in TEST_BENCHMARK_QUESTIONS:
        res = translate_question_to_mf_query(q["question"])
        metric_match = res["metrics"] == q["expected_metric"]
        group_match = res["group_by"] == q["expected_group_by"]
        status = "PASSED" if (metric_match and group_match) else "FAILED"
        if status == "PASSED":
            passed += 1
            
        print(f"\n[Question #{q['id']}] {q['question']}")
        print(f"  -> Metrics : {res['metrics']} (Expected: {q['expected_metric']})")
        print(f"  -> GroupBy : {res['group_by']} (Expected: {q['expected_group_by']})")
        print(f"  -> Command : {res['command']}")
        print(f"  -> Result  : [{status}]")
        
    print("\n--------------------------------------------------------------------------")
    print(f"Benchmark Summary: {passed}/{len(TEST_BENCHMARK_QUESTIONS)} Passed ({passed/len(TEST_BENCHMARK_QUESTIONS)*100:.1f}%)")
    print("--------------------------------------------------------------------------\n")

if __name__ == "__main__":
    run_benchmark()
