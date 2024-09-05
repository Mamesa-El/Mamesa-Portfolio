---
layout: page
title: Projects
permalink: /projects/
---

## Projects

### HuggingFace RESTful API Deployment
<div style="text-align: center;">
    <!-- Hugging Face -->
    <img src="https://user-images.githubusercontent.com/1393562/197941700-78283534-4e68-4429-bf94-dce7ab43a941.svg" width="7%" alt="Hugging Face">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- FAST API -->
    <img src="https://user-images.githubusercontent.com/1393562/190876570-16dff98d-ccea-4a57-86ef-a161539074d6.svg" width="7%" alt="Fast API">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- REDIS LOGO -->
    <img src="https://user-images.githubusercontent.com/1393562/190876644-501591b7-809b-469f-b039-bb1a287ed36f.svg" width="7%" alt="Redis Logo">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- KUBERNETES -->
    <img src="https://user-images.githubusercontent.com/1393562/190876683-9c9d4f44-b9b2-46f0-a631-308e5a079847.svg" width="7%" alt="Kubernetes">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- Azure -->
    <img src="https://user-images.githubusercontent.com/1393562/192114198-ac03d0ef-7fb7-4c12-aba6-2ee37fc2dcc8.svg" width="7%" alt="Azure">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- K6 -->
    <img src="https://user-images.githubusercontent.com/1393562/197683208-7a531396-6cf2-4703-8037-26e29935fc1a.svg" width="7%" alt="K6">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- Grafana -->
    <img src="https://user-images.githubusercontent.com/1393562/197682977-ff2ffb72-cd96-4f92-94d9-2624e29098ee.svg" width="7%" alt="Grafana">
</div>


In this project, I deployed a machine learning model using **Hugging Face transformers** on **Microsoft Azure Kubernetes Service (AKS)**. The model was made accessible via RESTful APIs, and I implemented **Prometheus** and **Grafana** for real-time monitoring of key performance metrics, such as request throughput and latency. The integration of **FastAPI** enabled rapid unit testing to ensure the robustness of the API endpoints.

#### Performance Overview

Using **Prometheus** and **Grafana** dashboards, I tracked and optimized resource usage while maintaining high performance under stress testing. The results of the testing revealed a system latency of under 10 microseconds and a throughput exceeding 100 requests per second.

The performance of the API was thoroughly tested using **k6.io** load testing. Below is a snapshot of the load test result:

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

### Data Analysis for Trending Content and Top Influencers on Social Media Platforms
<div style="text-align: center;">
    <!-- Python -->
    <img src="./Images/Python-logo-notext.svg" width="7%" alt="Hugging Face">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- Jupyter Notebook -->
    <img src="./Images/Jupyter_logo.png" width="7%" alt="Jypter">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- Github -->
    <img src="./Images/GitHub_Invertocat_Logo.png" width="7%" alt="Github">
</div>

This project analyzed social media influencers on platforms like Instagram, YouTube, and TikTok to understand engagement patterns and identify key factors contributing to influencer success. Using data from Kaggle, I focused on analyzing influencer categories, engagement metrics, and subscriber growth.
![Box Cox Transformation](./Social%20Median%20Influencer/Images/box_cox_transformation.png)
*Figure 1: The Box-Cox transformation was applied to normalize skewed data distributions for more accurate statistical analysis.*

![Top Genre](./Social%20Median%20Influencer/Images/Top%20Genres.png)
*Figure 2: Distribution of Top Influencers by Genre.*

**Key Insights**:
Dominant Categories: The Music and Music & Dance categories were the most popular (*shown in figure 2*), with Instagram and YouTube influencers in these categories having the highest total follower counts.

**Engagement Analysis**: There was a strong correlation between Authentic Engagement and Average Engagement on Instagram, indicating that influencers with high-quality interactions receive higher overall engagement.

**Platform Comparison**: Instagram was the top platform by total followers, followed by YouTube and TikTok.

**Technical Highlights**: Cleaned and normalized the dataset by removing duplicates and converting values with abbreviations (e.g., 'M', 'K') into numeric formats.
Applied Box-Cox Transformation to normalize skewed data distributions (*shown in figure 1*), improving the accuracy of correlation analysis and predictive modeling.
