# bbref-scraper
scraping win loss orders from basketball reference's playoff history page and calculating the probability of the observed win percentages for each win/loss order.

scraper and analysis code in code/, full history of win orders in results/nba_playoff_results.csv, full p-values in results/p_values.csv. Cleaned p values for blogpost.

Blogpost below!

## Background 

The Boston Celtics beat the Miami Heat on Game 6 of the NBA ECF last week, becoming just the fourth team to push a NBA series to seven games after losing the first three. 

Plenty of teams have come back from down 3-1 (13).  In around 25% of series that go 3-0, the losing team extends the series to 3-1. However, the losing team has never won the series after accumulating a three game deficit. 

For the Heat's sake (I hate the Celtics and thank god they lost the series), I wondered: "Is LLLW more of a death sentence compared to its 1-3 peers WLLL, LWLL, and LLWL?". In this post, I'll investigate how significant the order of wins and losses is (in NBA postseason history). 

## Analysis

Null Hypothesis: The order of wins and losses do not affect the outcome of the series.

Alternative Hypothesis: The order does affect the outcome of the series.

If H0 is true, we expect each permutation associated with some overall series record to have the same win percentage. For example, for all series that go 1-3, there are the four orderings listed above: WLLL, LWLL, LLWL, and (the dreaded?) LLLW. If the null hypothesis is true, no matter which ordering brings a team to 1-3, they can expect to win the series at the same rate (13/341) = 3.8%.

This analysis will be simple-- I'm going to assume for each possible record: 1-1, 1-2, 1-3, 2-1, 2-2, 2-3, 3-1, 3-2, 3-3*, that each possible ordering for a record is drawn from a binomial distribution of the overall win percent of that record, and see how likely it is to observe a win percentage as or more significant than the ordering's true win percent based on that.

A simple example is 3-3 and the corresponding LLLWWW record. There have been 147 NBA Game 7s so trivially we know the overall record is 147-147 (since there are always two teams at 3-3, and one loses and the other wins). 

Thus, we assume LLLWWW, which has occured 4 times, has its win percentage drawn from a binomial distribution B(4, .5). LLLWWW has a historical record of 0-4, which we would expect to see about 6.25% of the time (since we expect them to have a 50% chance of winning, like the overall record, and they flipped lose 3 times). Makes sense right? 

\* (series records with 4 or 0 excluded because there is only one possible ordering if one team hasn't won and a team with 4 wins has already won the series, so all permutations have 100% wr)

## Data 

I used bbref to get series outcomes for all series that have been played since 1947.

However, they didn't have the win loss order for each series so I wrote a simple page scraper to grab those and store them in a CSV. 

After that, for each win loss order, I got the probability that the overall record win percentage would generate a result as or more extreme as the observed win loss order win percentage. The full results are at the bottom of the page. 

Some interesting observations: 

#### 1. WWLL is really good (and LLWW is really bad). 

We can expect a 50% win rate at 2-2, but teams that win the first two tend to win 74.4% of the time across 130 games, good for the least likely entry on the table (p=2.54756088685077E-08). I would guess that home teams are more likely to reach WWLL due to home court advantage. 

Because of that, they might be more likely to win from this point because they are actually better (higher seeded, so more regular season wins). Further, they have home court advantage (which may be more impactful than normal in these series, since WWLL implies 4-0 for the home team). 

Nuggets vs. Suns hit this mark in the second round of the WCF this year, and the first seeded Nuggets, who have a reputation for the best home court advantage in the NBA, won in six games. 

#### 2. WL (and its siblings WLWL, WLWLWL) are pretty good too.

WL is good for a 58.8% win rate through 403 games, which we would only expect to see .04% of the time given a true 50% winrate.

The same reason as above might explain this, since some series were played as best of 3s long ago. 

Teams that attain WLWL have 61% of winning the series in 111 tries, which we expect to see 2.2% of the time with a true 50% win rate. WLWLWL has a 66% win rate over just 24 games, which we expect 15% of the time.

In the old best of five first round series and the 2-2-1-1-1 format (reintroduced in 2013), the higher seeded home team would head home for the last game of the series (or two of the last three). If home teams were more likely to win in this WLWL.. pattern, that might explain these observed win percentages. But I have no idea why they would choose to win and lose like this.

#### 3. The best way to go 3-3 is unclear.

Here are the 3-3s in order of winrate (excluding WWWLLL):

|Order |Win Percent|P value    |
|------|-----------|-----------|
|WWWLLL|1          |0.0625     |
|WWLWLL|0.777777778|0.1796875  |
|WWLLLW|0.769230769|0.092285156|
|WLLWWL|0.764705882|0.049041748|
|WWLLWL|0.705882353|0.02430651 |
|WLWLWL|0.666666667|0.151589632|
|LWWLWL|0.636363636|0.286278725|
|LWWWLL|0.636363636|0.548828125|
|LWLWWL|0.611111111|0.480682373|
|LWLLWW|0.571428571|0.790527344|
|WLWWLL|0.428571429|0.790527344|
|WLWLLW|0.388888889|0.480682373|
|WLLWLW|0.363636364|0.286278725|
|WLLLWW|0.363636364|0.548828125|
|LWLWLW|0.333333333|0.151589632|
|LLWWLW|0.294117647|0.02430651 |
|LWWLLW|0.235294118|0.049041748|
|LLWWWL|0.230769231|0.092285156|
|LLWLWW|0.222222222|0.1796875  |
|LLLWWW|0          |0.0625     |

It looks like the first two games predict the outcome of the series well. WW makes up most of the top quarter and LL makes up most of the bottom quarter. This is consistent with our home court advantage hypothesis. 

Contrary to our home court explanation, WWLLWL wins slightly less than WLLWWL-- which has a 76% win rate. If the higher seed goes WWLLWL, the home team will have won all six games with the higher seed heading home. We might expect that WWLLWL would be even more likely to win since it seems like home court predicts winning well in these series, but WLLWWL manages to edge it out. Philadelphia managed to beat the odds this year by losing to Boston in 7, landing in the 24% of teams that lose with this order.

## Conclusion

This was a fun but very simple analysis of NBA series outcomes. It seems that in a lot of cases, win orders are associated with the series outcome. I did not do any causal analysis, though that would be interesting to see. 

I speculate that there's a selection effect between seeding and win order, and that seeding/being the home team is actually related to the outcome. That would be an interesting place to throw matching or other stuff at. 


## Full Data

I would have liked to have made this sortable but right now my blogposts are stored as markdown. You can download the csv from the github link above and sort for yourself if you'd like though.


|Win Order|Record|Total_Winners|Total_Count|Observed Win Percentage|p-value               |Expected Win Percentage|
|---------|------|-------------|-----------|-----------------------|----------------------|-----------------------|
|L        |0-1   |201          |922        |0.21800433839479394    |1.0258344834068072    |0.21800433839479394    |
|W        |1-0   |721          |922        |0.7819956616052061     |1.0258344834068072    |0.7819956616052061     |
|LL       |0-2   |35           |519        |0.0674373795761079     |1.0496859933634437    |0.0674373795761079     |
|WW       |2-0   |484          |519        |0.9325626204238922     |1.0496859933634672    |0.9325626204238922     |
|WL       |1-1   |237          |403        |0.5880893300248139     |0.0004739146907029035 |0.5                    |
|LW       |1-1   |166          |403        |0.4119106699751861     |0.00047391469070280694|0.5                    |
|WLW      |2-1   |195          |246        |0.7926829268292683     |0.6266117635283333    |0.8066465256797583     |
|WWL      |2-1   |224          |259        |0.8648648648648649     |0.017564648571389396  |0.8066465256797583     |
|WLL      |1-2   |42           |157        |0.267515923566879      |0.02916290868403726   |0.1933534743202417     |
|LWL      |1-2   |51           |246        |0.2073170731707317     |0.6266117635283304    |0.1933534743202417     |
|LWW      |2-1   |115          |157        |0.732484076433121      |0.029162908684037713  |0.8066465256797583     |
|LLL      |0-3   |0            |222        |0.0                    |                      |                       |
|WWW      |3-0   |222          |222        |1.0                    |2.0                   |1.0                    |
|LLW      |1-2   |35           |259        |0.13513513513513514    |0.017564648571389826  |0.1933534743202417     |
|LWWW     |3-1   |65           |69         |0.9420289855072463     |0.5388003863971147    |0.9618528610354223     |
|WLWL     |2-2   |68           |111        |0.6126126126126126     |0.02229795480194796   |0.5                    |
|LLLW     |1-3   |0            |65         |0.0                    |0.15962160358432523   |0.03814713896457766    |
|WLLW     |2-2   |38           |77         |0.4935064935064935     |1.0                   |0.5                    |
|WWLL     |2-2   |96           |129        |0.7441860465116279     |2.547560895571621e-08 |0.5                    |
|WLLL     |1-3   |4            |69         |0.057971014492753624   |0.5388003863971145    |0.03814713896457766    |
|WWWL     |3-1   |65           |65         |1.0                    |0.1596216035843252    |0.9618528610354223     |
|LLWL     |1-3   |2            |130        |0.015384615384615385   |0.24644289007255832   |0.03814713896457766    |
|LLWW     |2-2   |33           |129        |0.2558139534883721     |2.547560886850772e-08 |0.5                    |
|LWWL     |2-2   |39           |77         |0.5064935064935064     |1.0                   |0.5                    |
|WLWW     |3-1   |95           |103        |0.9223300970873787     |0.08737034989754937   |0.9618528610354223     |
|LWLL     |1-3   |8            |103        |0.07766990291262135    |0.08737034989754955   |0.03814713896457766    |
|LWLW     |2-2   |43           |111        |0.38738738738738737    |0.022297954801947985  |0.5                    |
|WWLW     |3-1   |128          |130        |0.9846153846153847     |0.24644289007255837   |0.9618528610354223     |
|WLWWL    |3-2   |35           |43         |0.813953488372093      |0.48674946690963505   |0.860730593607306      |
|WLWLW    |3-2   |61           |69         |0.8840579710144928     |0.7273182819484023    |0.860730593607306      |
|WLWLL    |2-3   |7            |42         |0.16666666666666666    |0.7346375944319554    |0.13926940639269406    |
|LLWWW    |3-2   |23           |33         |0.696969696969697      |0.023769045312436496  |0.860730593607306      |
|WWLWL    |3-2   |32           |34         |0.9411764705882353     |0.2585934178571221    |0.860730593607306      |
|WLLWW    |3-2   |30           |34         |0.8823529411764706     |0.955898784791388     |0.860730593607306      |
|LLLWW    |2-3   |0            |17         |0.0                    |0.15623310734168802   |0.13926940639269406    |
|WLLWL    |2-3   |8            |43         |0.18604651162790697    |0.48674946690963594   |0.13926940639269406    |
|LLWLW    |2-3   |2            |34         |0.058823529411764705   |0.25859341785712214   |0.13926940639269406    |
|WWLLW    |3-2   |86           |96         |0.8958333333333334     |0.4030359137152748    |0.860730593607306      |
|WLLLW    |2-3   |4            |27         |0.14814814814814814    |1.060316114304678     |0.13926940639269406    |
|LWLWL    |2-3   |8            |69         |0.11594202898550725    |0.7273182819484033    |0.13926940639269406    |
|WWWLL    |3-2   |17           |17         |1.0                    |0.15623310734168805   |0.860730593607306      |
|LWWWL    |3-2   |23           |27         |0.8518518518518519     |1.0603161143046773    |0.860730593607306      |
|WWLLL    |2-3   |10           |33         |0.30303030303030304    |0.02376904531243662   |0.13926940639269406    |
|LWWLW    |3-2   |35           |43         |0.813953488372093      |0.48674946690963505   |0.860730593607306      |
|LWWLL    |2-3   |4            |34         |0.11764705882352941    |0.9558987847913878    |0.13926940639269406    |
|LWLWW    |3-2   |35           |42         |0.8333333333333334     |0.7346375944319542    |0.860730593607306      |
|LWLLW    |2-3   |8            |43         |0.18604651162790697    |0.48674946690963594   |0.13926940639269406    |
|LLWWL    |2-3   |10           |96         |0.10416666666666667    |0.4030359137152755    |0.13926940639269406    |
|WWLLWL   |3-3   |24           |34         |0.7058823529411765     |0.024306510109454393  |0.5                    |
|WWLLLW   |3-3   |10           |13         |0.7692307692307693     |0.09228515625         |0.5                    |
|WWLWLL   |3-3   |7            |9          |0.7777777777777778     |0.1796875             |0.5                    |
|WLWWLL   |3-3   |6            |14         |0.42857142857142855    |0.79052734375         |0.5                    |
|LWWWLL   |3-3   |7            |11         |0.6363636363636364     |0.548828125           |0.5                    |
|WLWLLW   |3-3   |7            |18         |0.3888888888888889     |0.480682373046875     |0.5                    |
|WLLWWL   |3-3   |13           |17         |0.7647058823529411     |0.049041748046875     |0.5                    |
|WLLWLW   |3-3   |8            |22         |0.36363636363636365    |0.28627872467041016   |0.5                    |
|WLLLWW   |3-3   |4            |11         |0.36363636363636365    |0.548828125           |0.5                    |
|LWWLWL   |3-3   |14           |22         |0.6363636363636364     |0.28627872467041016   |0.5                    |
|LWWLLW   |3-3   |4            |17         |0.23529411764705882    |0.049041748046875     |0.5                    |
|LWLWWL   |3-3   |11           |18         |0.6111111111111112     |0.480682373046875     |0.5                    |
|LWLWLW   |3-3   |8            |24         |0.3333333333333333     |0.15158963203430176   |0.5                    |
|LWLLWW   |3-3   |8            |14         |0.5714285714285714     |0.79052734375         |0.5                    |
|LLWWWL   |3-3   |3            |13         |0.23076923076923078    |0.09228515625         |0.5                    |
|LLWWLW   |3-3   |10           |34         |0.29411764705882354    |0.024306510109454393  |0.5                    |
|LLWLWW   |3-3   |2            |9          |0.2222222222222222     |0.1796875             |0.5                    |
|LLLWWW   |3-3   |0            |5          |0.0                    |0.0625                |0.5                    |
|WLWLWL   |3-3   |16           |24         |0.6666666666666666     |0.15158963203430176   |0.5                    |
|WWWLLL   |3-3   |5            |5          |1.0                    |0.0625                |0.5                    |


