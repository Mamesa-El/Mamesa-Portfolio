### Data Analysis for Trending Content and Top Influencers on Social Media Platforms
<div style="text-align: center;">
    <!-- Python -->
    <img src="../Images/Python-logo-notext.svg" width="7%" alt="Hugging Face">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- Jupyter Notebook -->
    <img src="../Images/Jupyter_logo.png" width="7%" alt="Jypter">
    <!-- PLUS SIGN -->
    <img src="https://user-images.githubusercontent.com/1393562/190876627-da2d09cb-5ca0-4480-8eb8-830bdc0ddf64.svg" width="7%" alt="Plus Sign">
    <!-- Github -->
    <img src="../Images/GitHub_Invertocat_Logo.png" width="7%" alt="Github">
</div>

This project analyzed social media influencers on platforms like Instagram, YouTube, and TikTok to understand engagement patterns and identify key factors contributing to influencer success. Using data from Kaggle, I focused on analyzing influencer categories, engagement metrics, and subscriber growth.
![Box Cox Transformation](./Images/box_cox_transformation.png)
*Figure 1: The Box-Cox transformation was applied to normalize skewed data distributions for more accurate statistical analysis.*

![Top Genre](./Images/Top%20Genres.png)
*Figure 2: Distribution of Top Influencers by Genre.*

**Key Insights**:
Dominant Categories: The Music and Music & Dance categories were the most popular (*shown in figure 2*), with Instagram and YouTube influencers in these categories having the highest total follower counts.

**Engagement Analysis**: There was a strong correlation between Authentic Engagement and Average Engagement on Instagram, indicating that influencers with high-quality interactions receive higher overall engagement.

**Platform Comparison**: Instagram was the top platform by total followers, followed by YouTube and TikTok.

**Technical Highlights**: Cleaned and normalized the dataset by removing duplicates and converting values with abbreviations (e.g., 'M', 'K') into numeric formats.
Applied Box-Cox Transformation to normalize skewed data distributions (*shown in figure 1*), improving the accuracy of correlation analysis and predictive modeling.
