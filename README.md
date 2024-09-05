# Data Scientist

#### Technical Skills:
- **Programming Language**: Python, R, SQL
- **Platforms & Tools**: Databricks, AWS SageMaker, Spark, Hadoop
- **Containerization & Orchestration**: Docker, Azure Kubernetes
- **LLM Techniques**: Prompted Engineering, Retriebal Augmented Generation (RAG)

## Education

- Master of Information and Data Science | University of Calfornia, Berkeley (_May 2022_)
- Bachelor of Science in Physics | Western Washington University (_July 2021_)

## Work Experience
**Data Scientist, Volt Lab Inc. | April, 2023 - February, 2024**
- Developed and managed machine learning algorithms using Scikit-Learn, NLP, and BERT for a spam
detection system, achieving an 80% F1 score through rigorous statistical analysis and model optimization.
- Designed and optimized SMS data pipelines using Python and SQL, integrating preprocessing, feature
engineering, and model selection techniques to achieve a 30% reduction in processing time.
- Maintained machine learning model lifecycle in AWS SageMaker, deploying models, managing batch
training, and securing endpoint access.
- Showcased strong written communication by authoring concise reports and presenting complex data
insights to non-technical teams, leading to significant reductions in client-generated spam.

**Data Analyst, Western Washington University | Sept 2019 - June, 2021**
- Analyzed spectroscopic data from 12 galaxy clusters using Python and Astropy to extract key properties,
applying anomaly detection methods to target extreme luminosity variations.
- Engineered scripts to efficiently analyze and visualize over 200,000 galaxies, developing practical ML
solutions that included properties and clustering analysis.

## Projects

### HuggingFace RESTful API Deployment

In this project, I deployed a machine learning model using **Hugging Face transformers** on **Microsoft Azure Kubernetes Service (AKS)**. The model was made accessible via RESTful APIs, and I implemented **Prometheus** and **Grafana** for real-time monitoring of key performance metrics, such as request throughput and latency. The integration of **FastAPI** enabled rapid unit testing to ensure the robustness of the API endpoints.

#### Performance Overview

Using **Prometheus** and **Grafana** dashboards, I tracked and optimized resource usage while maintaining high performance under stress testing. The results of the testing revealed a system latency of under 10 microseconds and a throughput exceeding 100 requests per second.

The performance of the API was thoroughly tested using **k6.io** load testing. Below is a snapshot of the load test result:
H
![K6 Load Test Results](./HuggingFace%20Restful%20API%20Deployment/grafana_image/K6%20Logs.png)

*Figure 1: Load test results showing HTTP request durations, latency, and throughput under heavy load.*

The figure above (Figure 1) showcases the **K6** load testing results, highlighting metrics such as request duration and iterations per virtual user. These metrics helped identify bottlenecks and optimize the system’s performance further.

#### Service Monitoring

To monitor the real-time performance and health of services, I used **Grafana dashboards** integrated with **Prometheus**. This allowed for detailed monitoring of incoming requests, latency, and throughput. Below is a key dashboard showing service performance:

![Service Workload Dashboard](./HuggingFace%20Restful%20API%20Deployment/grafana_image/SVC%20Service%20Workload.png)

*Figure 2: Service workload dashboard monitoring the latency and throughput for requests across various service workloads.*

Figure 2 illustrates the real-time performance of services, allowing me to track response times and throughput, which were crucial in optimizing resource allocation during peak times.

### Key Achievements

- **Latency:** Maintained latency under 10 microseconds during peak load times.
- **Throughput:** Consistently handled more than 100 requests per second.
- **Monitoring:** Implemented **Prometheus** and **Grafana** to track resource usage and service health.
- **Load Testing:** Leveraged **k6** for stress testing, optimizing the API for high-performance environments.


