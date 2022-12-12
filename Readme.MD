# Exploring Weekly Top10 on Netflix
## Background
<div style="text-align: justify">
Beginning from June 28 2021, Netflix commenced publishing every week from its library, a list of top 10 shows for the week, by hours watched. The site for this is https://top10.netflix.com/. In it, you can filter the list by category of shows (TV (English), TV (Non-English), Films (English), Films (Non-English)) to see the Global top 10 movies for the week. Besides the global top 10 list, the site also presents weekly top 10 by country. This however, does not show hours viewed. One can also download the list of global top 10 in Excel Formert at the end of the page. It is a cumulative of the top 10 shows from June 28, 2021 to date.</div>

## Research Interest
* We want to create a site which recommends trending movies to a visitor
* We want our visitor to be able to search by Genre or category for their top movie of interest

## Data Preparation
<div style="text-align: justify">We downloaded the global top 10 list from Netflix top10 site. As mentioned earlier, this list contains hours viewed, category, rank of the movie in top 10 and the number of times a movie has appeared on the top10 list. However, it has no information on the movie genre. We had to search the internet to populate this label for each movie to make our data more robust.</div>

## Approach
<div style="text-align: justify">We have used two variables to rank the movie list. One is by hours viewed, because the more hours a movie is viewed, the more likely it is a popular movie. We also relied on the number of times a movie appeared on the top10 list because that also signifies that it has a very wide audience and as such popular. Unfortunately, time did not permit us to add IMDB rating to enable a ranking by this criteria which seam to be the most globally accepted way of ranking shows.</div>

## Results
<div style="text-align: justify">Our dashboard presents two tabs, an overview and breakdown tab. The overview page has a visual that compares movie categories by the percentage each contributes to the total hours viewed. There is also a visual that shows the top movies by hours viewed. We have limited this to 50 using a slider. Similarly, there is a third visual that displays the top movies by the number of times they appeared in the top 10 list. This also is limited to 50. The last visual in this tab compares top 20 genres by hours viewed

The breakdown tab allows our visitors to filter by genre and category to see the top movies based on their selected filters. They can also click a checkbox to see a full list of their selection ranked according to hours viewed.</div>

## Conclusion
<div style="text-align: justify">Even though some movies stand out as overall best using our ranking criteria, each visitor will get a different result depending on their preferences </div>
