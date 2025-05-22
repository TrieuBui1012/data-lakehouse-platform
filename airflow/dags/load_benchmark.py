from datetime import timedelta
from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.utils import yaml
import os
import pendulum
from stackable.spark_kubernetes_sensor import SparkKubernetesSensor
from stackable.spark_kubernetes_operator import SparkKubernetesOperator


with DAG(  
    dag_id="load_benchmark",
    schedule_interval=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Bangkok"),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["example"],
    params={},
) as dag:

    def load_body_to_dict(body):
        try:
            body_dict = yaml.safe_load(body)
        except yaml.YAMLError as e:
            raise AirflowException(f"Exception when loading resource definition: {e}\n")
        return body_dict

    yaml_path = os.path.join(
        os.environ.get("AIRFLOW__CORE__DAGS_FOLDER", ""), "load_benchmark.yaml"
    )

    with open(yaml_path, "r") as file:
        crd = file.read()
    ns = "spark"

    document = load_body_to_dict(crd)
    application_name = "load-benchmark-" + pendulum.now('Asia/Bangkok').strftime(
        "%Y%m%d%H%M%S"
    )
    document.update({"metadata": {"name": application_name, "namespace": ns}})

    t1 = SparkKubernetesOperator(  
        task_id="load_benchmark_submit",
        namespace=ns,
        application_file=document,
        do_xcom_push=True,
        dag=dag,
    )

    t2 = SparkKubernetesSensor(  
        task_id="load_benchmark_monitor",
        namespace=ns,
        application_name="{{ task_instance.xcom_pull(task_ids='load_benchmark_submit')['metadata']['name'] }}",
        poke_interval=5,
        dag=dag,
    )

    t1 >> t2