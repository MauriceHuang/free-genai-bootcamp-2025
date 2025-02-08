# Prompt

As a Japanese teacher, your student will give you simple sentence in English, that has a pronoun, action, and object. e.g I walk to the door, She ate an apple and your will need to return the sentence in Japanese and identify the pronoun, action, and object in Hiragana and romanji.

# Initial Response

```
I understand that I'll be acting as a Japanese teacher analyzing sentences with pronouns, actions, and objects. I'll create a structured format for teaching these components.
For our example "I walk to the door":
Japanese Translation: わたし は ドア まで あるきます
Romaji: watashi wa doa made arukimasu
Sentence Components:
    1.	Pronoun (主語/しゅご)
    ▪	わたし (watashi) = I
    2.	Action/Verb (どうし)
    ▪	あるきます (arukimasu) = walk
    3.	Object (目的語/もくてきご)
    ▪	ドア (doa) = door
Note:
    •	は (wa) is a particle marking the subject
    •	まで (made) is a particle meaning "to/until"
Please provide your English sentence, and I'll break it down in the same way!
```

> The response is not structured to be placed into a structured object e.g JSON which what I am aiming for for tracking and student's performance evaluation.

# Prompt Iterations

### revised prompt
> As a Japanese teacher, your student will give you simple sentence in English, that has a pronoun, action, and object. e.g I walk to the door, She ate an apple and your will need to return the sentence in Japanese and identify the pronoun with any particle marking, action with any particle, and object with the unit. in Hiragana and romanji. Please response in table format with 2 rows and 3 columns. First row for Hiragana, second row for romanji. first column will be the pronoun with particle marking, second column will be for action with any particle and last column will be for the object.

### response 

>For the sentence "I take an apple":

| Pronoun + Particle | Action + Particle | Object + Particle |
| -------- | ------- | ------- |
| わたし は | とり を | りんご を |
| watashi wa | tori wo | ringo wo |


>For the sentence "I walk to the door":

| Pronoun + Particle | Action + Particle | Object + Particle |
| -------- | ------- | ------- |
| わたし は | あるき まで | ドア へ |
| watashi wa | aruki made | doa he |


### Thoughts
 - It will be nice if we are able to track all the vocabulary used and enhance with new vocabulary to strengthen the usage of vocabulary through series of recall.
 - I should give a level and have the llm to suggest a few new words each time that goes with the old vocabulary.

 ### revised prompt
> As a Japanese teacher, your student will give you simple sentence in English, that has a pronoun, action, and object. e.g I ate an apple, He jumped over a rock and your will need to return the sentence in Japanese and identify the pronoun with any particle marking, action with any particle, and object with the unit(a, an, two, three, this, that). in Hiragana and romanji. Please response in table format with 2 rows and 3 columns. First row for Hiragana, second row for romanji. first column will be the pronoun with particle marking, second column will be for action with any particle and last column will be for the object. Please suggest few new words for Pronoun, action or object not more than 2 for each for the student to include in the ongoing exercise.

### response
Let's take the sentence "I ate an apple" as an example. Here is the breakdown in Japanese:
| | Pronoun with particle | Action with particle | Object with unit |
| --- | --- | --- | --- |
| Hiragana | わたしが | を食べた | りんご一個 |
| Romanji | watashi ga | o tabeta | ringo ikko |

For the sentence "He jumped over a rock":
| | Pronoun with particle | Action with particle | Object with unit |
| --- | --- | --- | --- |
| Hiragana | かれが | を飛んだ | いしうつぼ一個 |
| Romanji | kare ga | o tobida | ishi utsubo ikko |

New words for the student to include in the exercise:
-  Pronoun: 私たち (watashitachi - we), 彼ら (karera - they)
-  Action: 走る (hashiru - to run), 見る (miru - to see)
-  Object: 本 (hon - book), 鏡 (kagami - mirror)

### Thoughts
- I like the suggestions of new words. 
- I will like to experiment at the end of each response to include json object that can be feed into the prompt in future to quickly get the llm up to speed to where the student is and what to focus on next.

