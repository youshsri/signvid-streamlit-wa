from nltk.translate.bleu_score import sentence_bleu
#Import the sentence_bleu function from the NLTK (Natural Language Toolkit) library

sub = "Inbound travel to the Philippines for foreign nationals and returning Filipinos who are non-overseas Filipino workers has been suspended for one month from March 20 until April 19. The decision was made following a directive from the Philippine National Task Force Against COVID-19 on Tuesday. The Philippine government has also ordered international inbound arrivals at Manila’s Ninoy Aquino International Airport shall be limited  to a maximum of 1500 passengers per day for all airlines combined from March 18 to April 19 The National Task Force noted, that the Philippines has recorded on March 15 a total of  5404 new cases of COVID-19 the highest daily spike in the last six months. As a result, the Philippines will suspend the entry of foreigners and returning overseas Filipinos who are non-OFWs. There are exemptions however, which include holders of 9(C) visas Medical repatriation and their escorts Distressed returning overseas Filipinos emergency and humanitarian cases Flight suspensions"
#These are subtitles written by the publisher of the YouTube Video

grab = "Inbound travel to the Philippines for foreign nationals and returning Filipinos for non-overseas Filipino workers suspended for one month from March 20 until April 19. The decision was made following a director from the Philippine National Task Force again good 19 on Tuesday. The Philippine government has also ordered international inbound arrivals at Manila's ninoy Aquino International Airport to a maximum of 1500 passengers per day for all airlines combined from March 18 to April 19 The National Task Force noted that the film has recorded on March 15 at total of 5404 new cases of COVID-19 the highest daily spike in the last six months As a result the film will suspend the entry of foreign and returning overseas Filipinos who are non-OFWs There are exemptions however which include holders 90 visas Medical repatriation and their escorts Distressed returning overseas Filipinos emergency and humanitarian cases and fly pensions"
#This is the string of text that our program prompted


ref = sub.split()

reference = []

reference.append(ref)

candidate = grab.split()
#Line 11 to 17 changes the text into the right format for BLEU testing function

score = sentence_bleu(reference, candidate)
#Calculate BLEU score

print("Our BLEU score is: ", score)
#Printing results