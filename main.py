from loader import DataManager
from model.model import NewsSummarizationModel
import os

example_text = '''Shares of Google parent company Alphabet rose more than 9% after the company reported second-quarter earnings that beat estimates Thursday <PUNCT> Alphabet said its board of directors approved a repurchase of up to an additional $25 billion of its Class C capital stock <PUNCT> On a call with analysts, CFO Ruth Porat said the capital would be used to support growth and acquisitions and investments <PUNCT> Here are the key numbers: Earnings per share: $14.21 per share, ex-items, vs. $11.30 per share expected, per Refinitiv survey of analysts Revenue: $38.94 billion, vs. $38.15 billion expected, per Refinitiv Traffic acquisition costs: $7.24 billion, vs. $7.27 billion, according to StreetAccount Paid clicks on Google properties from Q2 2018 to Q2 2019: +28% Cost-per-click on Google properties from Q2 2018 to Q2 2019: -11% Alphabet beat analysts’ expectations on revenue and EPS but had even lower traffic acquisition costs (TAC) than analysts were hoping for <PUNCT> The metric represents the payments Google makes to companies like Apple for its search engine to be the default browser on their devices <PUNCT> Google reported advertising revenue of $32.6 billion for the second quarter, compared to $28.09 billion during the same period last year <PUNCT> Google’s other revenue, which includes hardware like its Pixel phones and cloud products, came in at $6.18 billion compared to $4.43 billion during last year’s quarter <PUNCT> Porat said on the earnings call that cloud revenue made up the majority of this segment and was the third largest driver of overall Alphabet revenue growth <PUNCT> Google recently installed a new cloud boss, Thomas Kurian, who has been charged with growing the business and has already made some splashy acquisitions, including analytics company Looker <PUNCT> On the earnings call, Google CEO Sundar Pichai said the cloud business reached an annual revenue run rate of over $8 billion <PUNCT> Google said in February 2018 that its cloud business was bringing in $1 billion dollars per quarter, its first disclosure of Google Cloud revenue <PUNCT> Pichai said the company wants to triple its cloud salesforce over the next few years <PUNCT> Alphabet said its revenue from "other bets," which includes its subsidiaries outside of Google like the self-driving car company Waymo, came in at $162 million compared to $145 million in the year-ago quarter <PUNCT> TAC as a percentage of Google advertising revenues was slightly lower this year compared to the previous year’s quarter at 22% compared to 23% in 2018 <PUNCT> That means the amount Google has to pay other companies to make its service the default is becoming a less significant proportion compared to its advertising revenue <PUNCT> It's a key figure that analysts and investors look at to assess the health of Google’s business <PUNCT> Google saw a 28% increase in paid clicks on its properties in Q2 of 2019 compared to the same quarter last year <PUNCT> It also saw an 11% decrease in cost-per-click on Google properties over that same period <PUNCT> Last quarter, shares of Alphabet tumbled when Google reported decelerating revenue growth, which it had blamed largely on YouTube <PUNCT> But this quarter, Porat said YouTube’s revenue was strong <PUNCT> While the company does not break out YouTube results, Porat provided some limited details on Thursday’s earnings call <PUNCT> “YouTube was again the second largest contributor of revenue growth, and [we’re] really pleased with the ongoing momentum that we’re seeing here,” Porat said <PUNCT> Porat clarified that her assessment that deceleration in YouTube click growth contributed to overall slowing revenue growth was not the result of removing content from its platform that violated its policies. “The click and CPC growth were unrelated to actions on policy enforcement,” Porat said of YouTube <PUNCT> Google now faces even broader threats to its business under the eye of US and foreign antitrust regulators <PUNCT> The US Department of Justice announced Tuesday it's opening a broad antitrust review of big tech companies <PUNCT> Though it did not name specific companies, the department said it will review the practices of online platforms dominating areas including internet search <PUNCT> Google has about 90% market share in internet search in the US In May, The Wall Street Journal reported the DOJ is planning a separate antitrust probe into Google <PUNCT> Last quarter, Alphabet recorded a European Commission fine of $1.7 billion as a settlement for stifling competition in the online ad sector <PUNCT> In June, the company said it had begun to appeal the fine <PUNCT> Asked about the regulatory environment, Pichai told analysts that it has dealt with scrutiny before and said, “To the extent we have to answer questions, we will do so constructively <PUNCT> "'''

def main():
    manager = DataManager(saved_dir='./data')
    model = NewsSummarizationModel(manager)
    model.build_model()
    model.model.summary()
    # model.plot_model()
    print('training...')
    model.train(epochs=2)
    model.save(os.getcwd(), 'cnbc')
    # model.load('./trained_model/cnbc-overall.h5', './trained_model/cnbc-encoder.h5', './trained_model/cnbc-decoder.h5')
    print(model.evaluate())
    print(model.infer(example_text))

if __name__ == '__main__':
    main()