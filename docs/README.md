# 273: Deuce to Seven Triple Draw
A variant of poker which the normal hand rankings are inverted. The best hand would be `7-5-4-3-2`. Exploring strategy, statistics, and game theory through simulation.


## Deliverables
Simulation-based results that explore the odds of drawing to certain hands based on how many rounds are left and how many opponents are available. Direct math based calculations on outs are available for many situations, but simulations allow for implementing opponent strategy models. We will look to answer questions like:
- How should our play be when our opponent only continues with a 2 and will stay pat with a smooth 9 or better after 1 draw?
- Is it better to bluff 7-7-5-2-2 (since you have seen cards others need) or draw 2? How often do you get there?
- With most equity being realized when playing heads-up, are there hands strong enough to encourage more players?


### Single Draw to smooth 7, 8, 9, T, J
<img src="./images/single/JT987_432.png" width="720px">
This chart shows the odds of not losing (wins + draws) when you have a hand (horizontal axis) and your opponent is taking a single draw with one of the following hands: 7432, 8432, 9432, T432, J432.

For instance, you can find when you are holding `T-8-6-4-2`, you won't lose 60% of the time against `7-4-3-2` drawing 1. Let's calculate the odds in a single-draw situation compared with our simulated results.

With 9 cards shown, there are 43 remaining.
<table>
    <tr><td>Hand</td><td>Outs</td><td>Odds</td><td>Simulation</td><td>Difference</td></tr>
    <tr><td>7-4-3-2</td><td>
        <table>
            <tr><td>5-5-5-5</td><td>6-6-6</td></tr>
            <tr><td>8-8-8</td><td>9-9-9-9</td></tr>
            <tr><td>T-T-T</td><td>&nbsp;</td></tr>
        </table>
    </td><td>1 - <b>17</b>/43<br/>= <b>60.47%</b></td><td><b>60.23%</b></td><td>0.24%</td></tr>
    <tr><td>8-4-3-2</td><td>
        <table>
            <tr><td>5-5-5-5</td><td>6-6-6</td></tr>
            <tr><td>7-7-7-7</td><td>9-9-9-9</td></tr>
            <tr><td>T-T-T</td><td>&nbsp;</td></tr>
        </table>
    </td><td>1 - <b>18</b>/43<br/>= <b>58.14%</b></td><td><b>58.32%</b></td><td>0.18%</td></tr>
</table>

With 43 cards remaining, it makes sense how each out represents `2.33%` equity. This will become more valuable later when multiple rounds of drawing allow us to gain additional information.


### Double Draw to smooth 4, 5, 6, 7, 8, 9, T, J
<img src="./images/double/T987654_32.png" width="720px">

## Deuce to Seven, Triple Draw Rules
### Hand Rankings

### Structure

