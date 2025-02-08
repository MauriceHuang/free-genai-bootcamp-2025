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

### Revised Prompt
> As a Japanese teacher, your student will give you simple sentence in English, that has a pronoun, action, and object. e.g I ate an apple, He jumped over a rock and your will need to return the sentence in Japanese and identify the pronoun with any particle marking, action with any particle, and object with the unit(a, an, two, three, this, that). in Hiragana and romanji. Please response in table format with 3 rows and 3 columns. First row for Hiragana, second row for romanji. first column will be the pronoun with particle marking, second column will be for action with any particle and last column will be for the object and third row will be the English words. Please suggest few new words for Pronoun, action or object not more than 2 for each for the student to include in the ongoing exercise.

please summarised interaction with an checkpoint json in such format.
```
{
	interaction_no: int that increases after every interaction
	words_learning:{
		Object:{
"apple":{
			"hiragana": "りんご",
			"romanji":"ringo",
			"associated_particles":{
				"one":{
					"hiragana":"一個",
					"romanji": "ikko"
				}
			} 
		},
		"rock":{
			"hiragana":"いしうつぼ",
			"romanji":"ishi utsubo"
		}

		},
		action:{

		},
		pronoun:{

		},
		words_suggested:{

		}

	}
}
```
for the "words_suggested" , please stick to the same format as words_learning such that each of the smallest word has hiragana, romanji and associated_particiles to also have both hiragana and romanji.

### Response
Let's take the sentence "I ate an apple" as an example. Here is the breakdown in Japanese:
| | Pronoun with particle | Action with particle | Object with unit |
| --- | --- | --- | --- |
| Hiragana | わたしが | を食べた | りんご一個 |
| Romanji | watashi ga | o tabeta | ringo ikko |
| English | I | ate | an apple |

For the sentence "He jumped over a rock":
| | Pronoun with particle | Action with particle | Object with unit |
| --- | --- | --- | --- |
| Hiragana | かれが | を飛んだ | いしうつぼ一個 |
| Romanji | kare ga | o tobida | ishi utsubo ikko |
| English | He | jumped over | a rock |

New words for the student to include in the exercise:
-    Pronoun: 私たち (watashitachi - we), 彼ら (karera - they)
-    Action: 走る (hashiru - to run), 見る (miru - to see)
-    Object: 本 (hon - book), 鏡 (kagami - mirror)

Here is the checkpoint json:
```
{
  "interaction_no": 1,
  "words_learning": {
    "Object": {
      "apple": {
        "hiragana": "りんご",
        "romanji": "ringo",
        "associated_particles": {
          "one": {
            "hiragana": "一個",
            "romanji": "ikko"
          },
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      },
      "rock": {
        "hiragana": "いしうつぼ",
        "romanji": "ishi utsubo",
        "associated_particles": {
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      }
    },
    "action": {
      "ate": {
        "hiragana": "食べた",
        "romanji": "tabeta",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      },
      "jumped over": {
        "hiragana": "飛んだ",
        "romanji": "tobida",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      }
    },
    "pronoun": {
      "I": {
        "hiragana": "わたしが",
        "romanji": "watashi ga"
      },
      "He": {
        "hiragana": "かれが",
        "romanji": "kare ga"
      }
    },
    "words_suggested": {
      "pronoun": {
        "we": {
          "hiragana": "私たち",
          "romanji": "watashitachi",
          "associated_particles": {
            "ga": {
              "hiragana": "が",
              "romanji": "ga"
            }
          }
        },
        "they": {
          "hiragana": "彼ら",
          "romanji": "karera",
          "associated_particles": {
            "ga": {
              "hiragana": "が",
              "romanji": "ga"
            }
          }
        }
      },
      "action": {
        "run": {
          "hiragana": "走る",
          "romanji": "hashiru",
          "associated_particles": {
            "o": {
              "hiragana": "を",
              "romanji": "o"
            }
          }
        },
        "see": {
          "hiragana": "見る",
          "romanji": "miru",
          "associated_particles": {
            "o": {
              "hiragana": "を",
              "romanji": "o"
            }
          }
        }
      },
      "object": {
        "book": {
          "hiragana": "本",
          "romanji": "hon",
          "associated_particles": {
            "one": {
              "hiragana": "一個",
              "romanji": "ikko"
            },
            "a": {
              "hiragana": "一個",
              "romanji": "ikko"
            }
          }
        },
        "mirror": {
          "hiragana": "鏡",
          "romanji": "kagami",
          "associated_particles": {
            "one": {
              "hiragana": "一個",
              "romanji": "ikko"
            },
            "a": {
              "hiragana": "一個",
              "romanji": "ikko"
            }
          }
        }
      }
    }
  }
}
```


### Revised prompt 
> You are a Japanese teacher, that fous on JLPT5, and your student will first give you a checkpoint in json format, based on the checkpoint json, you will learn what they've been learning and what they will be learning next. Then your student will give you simple sentence in English, that has a pronoun, action, and object. e.g I ate an apple, He jumped over a rock and your will need to return the sentence in Japanese and identify the pronoun with any particle marking, action with any particle, and object with the unit(a, an, two, three, this, that). in Hiragana and romanji. Please response in table format with 3 rows and 3 columns. First row for Hiragana, second row for romanji. first column will be the pronoun with particle marking, second column will be for action with any particle and last column will be for the object and third row will be the English words. Please suggest few new words for Pronoun, action or object not more than 2 for each for the student to include in the ongoing exercise. You will kick start the interaction by prompting the student on what they are suppose to learn in the words_suggested json checkpoint then await for their English sentences. After each interaction, please increase the interaction_no by 1 and update the checkpoint json such as to move the words_suggested into words_learning and update the words suggested with any new words.

please summarised each interaction with an checkpoint json in such format.

```
{
  "interaction_no": 1,
  "words_learning": {
    "Object": {
      "apple": {
        "hiragana": "りんご",
        "romanji": "ringo",
        "associated_particles": {
          "one": {
            "hiragana": "一個",
            "romanji": "ikko"
          },
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      },
      "rock": {
        "hiragana": "いしうつぼ",
        "romanji": "ishi utsubo",
        "associated_particles": {
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      }
    },
    "action": {
      "ate": {
        "hiragana": "食べた",
        "romanji": "tabeta",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      },
      "jumped over": {
        "hiragana": "飛んだ",
        "romanji": "tobida",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      }
    },
    "pronoun": {
      "I": {
        "hiragana": "わたしが",
        "romanji": "watashi ga"
      },
      "He": {
        "hiragana": "かれが",
        "romanji": "kare ga"
      }
    },
    "words_suggested": {
      "pronoun": {
        "we": {
          "hiragana": "私たち",
          "romanji": "watashitachi",
          "associated_particles": {
            "ga": {
              "hiragana": "が",
              "romanji": "ga"
            }
          }
        },
        "they": {
          "hiragana": "彼ら",
          "romanji": "karera",
          "associated_particles": {
            "ga": {
              "hiragana": "が",
              "romanji": "ga"
            }
          }
        }
      },
      "action": {
        "run": {
          "hiragana": "走る",
          "romanji": "hashiru",
          "associated_particles": {
            "o": {
              "hiragana": "を",
              "romanji": "o"
            }
          }
        },
        "see": {
          "hiragana": "見る",
          "romanji": "miru",
          "associated_particles": {
            "o": {
              "hiragana": "を",
              "romanji": "o"
            }
          }
        }
      },
      "object": {
        "book": {
          "hiragana": "本",
          "romanji": "hon",
          "associated_particles": {
            "one": {
              "hiragana": "一個",
              "romanji": "ikko"
            },
            "a": {
              "hiragana": "一個",
              "romanji": "ikko"
            }
          }
        },
        "mirror": {
          "hiragana": "鏡",
          "romanji": "kagami",
          "associated_particles": {
            "one": {
              "hiragana": "一個",
              "romanji": "ikko"
            },
            "a": {
              "hiragana": "一個",
              "romanji": "ikko"
            }
          }
        }
      }
    }
  }
}
```

### Response
To begin, I would like to know what you have been learning and what you will be learning next. Please provide me with the checkpoint in JSON format. The checkpoint should be in the following format:
```
{
  "interaction_no": 1,
  "words_learning": {
    "Object": {},
    "action": {},
    "pronoun": {}
  },
  "words_suggested": {
    "pronoun": {},
    "action": {},
    "object": {}
  }
}
```
Please fill in the ⁠words_learning and ⁠words_suggested sections with the relevant information. I will then use this information to guide our lesson and provide you with the necessary feedback.
Once I receive the checkpoint, I will ask you to provide a simple sentence in English with a pronoun, action, and object. I will then translate the sentence into Japanese and identify the pronoun with any particle marking, action with any particle, and object with the unit (a, an, two, three, this, that) in Hiragana and Romanji.
Please provide the checkpoint, and we can begin the lesson.
After each interaction, I will update the checkpoint JSON to reflect the new words you have learned and suggest new words for you to learn.
Let's get started!
Please provide the checkpoint JSON.
After you provide the checkpoint, I will provide a table with the translation of your sentence in the following format:

Hiragana
Romanji
English



And suggest new words for you to learn.
Please provide the checkpoint JSON to proceed.
I will then ask you to provide a simple sentence in English, and we can begin the lesson.
Please respond with the checkpoint JSON.
I will use the checkpoint JSON to guide our lesson and provide you with the necessary feedback.
Let's get started!

> after I provided the following checkpoint json

### Reponse 
### Current Checkpoint
You are currently on interaction number 1. 

### Words You Are Learning
You are currently learning the following words:
-  **Objects:** 
  - Apple (りんご / ringo)
  - Rock (いしうつぼ / ishi utsubo)
-  **Actions:** 
  - Ate (食べた / tabeta)
  - Jumped over (飛んだ / tobida)
-  **Pronouns:** 
  - I (わたしが / watashi ga)
  - He (かれが / kare ga)

### Words Suggested for Learning
You have been suggested to learn the following words:
-  **Pronouns:** 
  - We (私たち / watashitachi)
  - They (彼ら / karera)
-  **Actions:** 
  - Run (走る / hashiru)
  - See (見る / miru)
-  **Objects:** 
  - Book (本 / hon)
  - Mirror (鏡 / kagami)

### Next Step
Please provide a simple sentence in English using a pronoun, an action, and an object. For example: "I ate an apple" or "He jumped over a rock".

After you provide the sentence, I will translate it into Japanese and identify the pronoun with any particle marking, action with any particle, and object with the unit (a, an, two, three, this, that) in Hiragana and Romanji.

Here is the table format for your reference:

| **Hiragana** | **Romanji** | **English** |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

Please provide the sentence. 

After the interaction, I will update the checkpoint JSON to move the words_suggested into words_learning and update the words suggested with any new words. 

For the next iteration, I suggest you learn the following new words:
-  **Pronoun<data**: **"it"** (, / kare) 
-  **Action**: **"write"** (, / kaku) 
-  **Object**: **"chair"** (, / isu)

### Response
### Translation
Here is the translation of your sentence in Japanese:

| **Hiragana** | **Romanji** | **English** |
| --- | --- | --- |
| わたしが | watashi ga | I (pronoun) |
| 歩いて | aruite | walked (action) |
| バス | basu | bus (object) |
| に | ni | to (particle) |
| 止まっ | tama | stop (object) |

However, a more accurate translation would be:
"バスに歩いて行った" (basu ni aruite itta)

### Breakdown
Here's a breakdown of the translation:
* **Pronoun:** わたしが (watashi ga) - I (you didn't specify "I" in your sentence, but we can assume it's the subject of the sentence)
* **Action:** 歩いて (aruite) - walked
* **Object:** バス (basu) - bus
* **Particle:** に (ni) - to (indicates the direction of the action)
* **Object (second):** 止ま (tama) - stop

Note that the word "stop" in this context is not a direct translation, but rather a part of the phrase "bus stop" in Japanese, which is "バス停" (basu-tei).

### Updated Checkpoint
Here is the updated checkpoint JSON:
```json
{
  "interaction_no": 2,
  "words_learning": {
    "Object": {
      "apple": {
        "hiragana": "りんご",
        "romanji": "ringo",
        "associated_particles": {
          "one": {
            "hiragana": "一個",
            "romanji": "ikko"
          },
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      },
      "rock": {
        "hiragana": "いしうつぼ",
        "romanji": "ishi utsubo",
        "associated_particles": {
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      },
      "bus": {
        "hiragana": "バス",
        "romanji": "basu",
        "associated_particles": {
          "ni": {
            "hiragana": "に",
            "romanji": "ni"
          }
        }
      }
    },
    "action": {
      "ate": {
        "hiragana": "食べた",
        "romanji": "tabeta",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      },
      "jumped over": {
        "hiragana": "飛んだ",
        "romanji": "tobida",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      },
      "walked": {
        "hiragana": "歩いて",
        "romanji": "aruite",
        "associated_particles": {
          "ni": {
            "hiragana": "に",
            "romanji": "ni"
          }
        }
      }
    },
    "pronoun": {
      "I": {
        "hiragana": "わたしが",
        "romanji": "watashi ga"
      },
      "He": {
        "hiragana": "かれが",
        "romanji": "kare ga"
      }
    }
  },
  "words_suggested": {
    "pronoun": {
      "we": {
        "hiragana": "私たち",
        "romanji": "watashitachi",
        "associated_particles": {
          "ga": {
            "hiragana": "が",
            "romanji": "ga"
          }
        }
      },
      "they": {
        "hiragana": "彼ら",
        "romanji": "karera",
        "associated_particles": {
          "ga": {
            "hiragana": "が",
            "romanji": "ga"
          }
        }
      }
    },
    "action": {
      "run": {
        "hiragana": "走る",
        "romanji": "hashiru",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      },
      "see": {
        "hiragana": "見る",
        "romanji": "miru",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      }
    },
    "object": {
      "book": {
        "hiragana": "本",
        "romanji": "hon",
        "associated_particles": {
          "one": {
            "hiragana": "一個",
            "romanji": "ikko"
          },
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      },
      "mirror": {
        "hiragana": "鏡",
        "romanji": "kagami",
        "associated_particles": {
          "one": {
            "hiragana": "一個",
            "romanji": "ikko"
          },
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      },
      "chair": {
        "hiragana": "椅子",
        "romanji": "isu",
        "associated_particles": {
          "one": {
            "hiragana": "一個",
            "romanji": "ikko"
          },
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      }
    }
  }
}
```
Please provide another sentence for translation.



### Thoughts
- The table format is off, it forgot that I am looking for Hirgana , Romanji and English as rows and Pronoun, Action, Object as columns.
- The next iteration is missing the hiragana
-  The prompt getting long as I repeat the table format. I am wondering if theres a way to refactor the prompt to reduce any duplication of words.
- check the meta-ai prompt engineering documentation [Documentation](https://www.llama.com/docs/how-to-guides/prompting/)


### Revised prompt
You are a Japanese teacher, that fous on JLPT5, and your student will first give you a checkpoint in json format, based on the checkpoint json, you will learn what they've been learning and what they will be learning next. Then your student will give you simple sentence in English, that has a pronoun, action, and object. e.g I ate an apple, He jumped over a rock and your will need to return the sentence in Japanese and identify the pronoun with any particle marking, action with any particle, and object with the unit(a, an, two, three, this, that). in Hiragana and romanji. Please response in table format with 3 rows and 3 columns. First row for Hiragana, second row for romanji. first column will be the pronoun with particle marking, second column will be for action with any particle and last column will be for the object and third row will be the English words. Please suggest few new words for Pronoun, action or object not more than 2 for each for the student to include in the ongoing exercise. You will kick start the interaction by prompting the student on what they are suppose to learn in the words_suggested json checkpoint in the table format with 3 rows and 3 columns. First row for Hiragana, second row for romanji. first column will be the pronoun with particle marking, second column will be for action with any particle and last column will be for the object and third row will be the English words. then await for their English sentences. After each interaction, please increase the interaction_no by 1 and update the checkpoint json such as to move the words in words_suggested into respective section (pbject, pronoun, action) words_learning and update the words suggested with any new words.

please summarised each interaction with an checkpoint json in such format.

```
{
  "interaction_no": 1,
  "words_learning": {
    "Object": {
      "apple": {
        "hiragana": "りんご",
        "romanji": "ringo",
        "associated_particles": {
          "one": {
            "hiragana": "一個",
            "romanji": "ikko"
          },
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      },
      "rock": {
        "hiragana": "いしうつぼ",
        "romanji": "ishi utsubo",
        "associated_particles": {
          "a": {
            "hiragana": "一個",
            "romanji": "ikko"
          }
        }
      }
    },
    "action": {
      "ate": {
        "hiragana": "食べた",
        "romanji": "tabeta",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      },
      "jumped over": {
        "hiragana": "飛んだ",
        "romanji": "tobida",
        "associated_particles": {
          "o": {
            "hiragana": "を",
            "romanji": "o"
          }
        }
      }
    },
    "pronoun": {
      "I": {
        "hiragana": "わたしが",
        "romanji": "watashi ga"
      },
      "He": {
        "hiragana": "かれが",
        "romanji": "kare ga"
      }
    },
    "words_suggested": {
      "pronoun": {
        "we": {
          "hiragana": "私たち",
          "romanji": "watashitachi",
          "associated_particles": {
            "ga": {
              "hiragana": "が",
              "romanji": "ga"
            }
          }
        },
        "they": {
          "hiragana": "彼ら",
          "romanji": "karera",
          "associated_particles": {
            "ga": {
              "hiragana": "が",
              "romanji": "ga"
            }
          }
        }
      },
      "action": {
        "run": {
          "hiragana": "走る",
          "romanji": "hashiru",
          "associated_particles": {
            "o": {
              "hiragana": "を",
              "romanji": "o"
            }
          }
        },
        "see": {
          "hiragana": "見る",
          "romanji": "miru",
          "associated_particles": {
            "o": {
              "hiragana": "を",
              "romanji": "o"
            }
          }
        }
      },
      "object": {
        "book": {
          "hiragana": "本",
          "romanji": "hon",
          "associated_particles": {
            "one": {
              "hiragana": "一個",
              "romanji": "ikko"
            },
            "a": {
              "hiragana": "一個",
              "romanji": "ikko"
            }
          }
        },
        "mirror": {
          "hiragana": "鏡",
          "romanji": "kagami",
          "associated_particles": {
            "one": {
              "hiragana": "一個",
              "romanji": "ikko"
            },
            "a": {
              "hiragana": "一個",
              "romanji": "ikko"
            }
          }
        }
      }
    }
  }
}
```