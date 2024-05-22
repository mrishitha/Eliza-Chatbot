#!/usr/bin/env python
# coding: utf-8

# # AIT526 - 001 - Natural Language Processing
# # Professor Lindi Liao
# 
# ## Programming Assignment - 1
# 
# #### Team Members:
# Hanishka Reddy
# Meghana Katta
# Rishitha Madipelli
# 
# 
# #### Date: 02/04/2024
# 
# 

# In[ ]:


#pip install gibberish_detector


# In[ ]:



import re
import random
from gibberish_detector import detector

Detector = detector.create_from_model('/Users/madipellirishitha/Desktop/MS/Eliza/big.model')


# Regex patterns for transforming user statements to questions
transformation_rules = {
    r'(stressed|overwhelmed|anxious)': [
        "It sounds like you're experiencing stress. What's been happening that makes you feel this way?",
        "Stress can be overwhelming. Can you identify specific situations contributing to these feelings?",
        "It's important to manage stress for your well-being. What's on your mind that's causing concern?"
    ],
    r'(happy|joyful|glad)': [
        "Hearing you're feeling happy is wonderful. What's been contributing to your positive mood lately?",
        "It's great to know you're in good spirits. What events or thoughts have led to this happiness?",
        "Happiness is crucial to a fulfilling life. What's been bringing you joy recently?"
    ],
    r'(mad|angry|furious)': [
        "Feeling angry is a natural response to many situations. What specifically has been bothering you?",
        "Anger often signifies a need for change. Can you share what's been making you feel this way?",
        "Let's discuss the reasons behind your anger. What's happened recently to evoke these feelings?"
    ],
    r'(lonely|isolated|alone)': [
        "Dealing with loneliness can be tough. Are there specific reasons you're feeling this way?",
        "Loneliness can weigh heavily. How have you been coping with these feelings?",
        "Feeling lonely is challenging. What do you think has been contributing to this sense of isolation?"
    ],
    r'(confused|uncertain|unsure)': [
        "Confusion can stem from many sources. Can you share more about what's causing these feelings?",
        "Uncertainty can be unsettling. What's unclear for you at the moment?",
        "Feeling unsure is a part of many decisions. Can you describe what you're deliberating on?"
    ],
    r'(tired|exhausted|worn out)': [
        "Tiredness can affect every part of life. What's been contributing to your feelings of fatigue?",
        "It's tough to feel drained. Can you share more about what's been taxing you recently?",
        "Chronic tiredness is hard to bear. What do you think is the main cause of your exhaustion?"
    ],
    r'(bored|uninterested|disengaged)': [
        "Feeling bored can indicate a need for change. What's been lacking in excitement for you?",
        "Boredom can be an opportunity to explore new interests. What haven't you explored yet that might interest you?",
        "Let's find ways to alleviate boredom. What activities or hobbies usually engage you?"
    ],
    r'(crave)':["Why don't you tell me more about your cravings?"],
    r'I need (.*)': [
        "It's interesting that you mention needing {0}. Could you explore that desire a bit more?",
        "Getting {0} seems important to you. How do you think it would benefit you?",
        "You're focused on needing {0}. What makes it significant for you?"
    ],
    r'Why don\'?t you ([^\?]*)\??': [
        "You're curious about my actions regarding {0}. What outcome are you envisioning?",
        "The possibility of me doing {0} intrigues you. Why is that?",
        "Your interest in whether I'd {0} is noted. What are your thoughts on it?"
    ],
    r'Why can\'?t I ([^\?]*)\??': [
        "You're questioning your ability to {0}. What obstacles do you feel are in your way?",
        "Imagining that you could {0}, what steps would you take next?",
        "Your question about not being able to {0} is quite profound. Have you taken time to reflect on this?"
    ],
    r'I can\'?t (.*)': [
        "Saying you can't {0} speaks volumes. What do you believe is stopping you?",
        "The thought of trying to {0} and feeling you can't is challenging. What might help you overcome this?",
        "Considerations around your belief that you can't {0} are worth exploring. What insights do you have?"
    ],
    r'I am (.*)': [
        "Coming to me as someone who is {0} tells me a lot. How does this identity shape your experiences?",
        "Being {0} for some time now, how has this influenced your perspective?",
        "Your feelings of being {0} are important. How does this affect you day to day?"
    ],
    r'I\'?m (.*)': [
        "Feeling {0} can have a big impact. How do you cope with this?",
        "Enjoying being {0} is an aspect of your life. What does it bring to you?",
        "You've shared that you're {0}. What does this mean for you in your life?"
    ],
    r'Are you ([^\?]*)\??': [
        "Whether I am {0} or not, how does that resonate with you?",
        "You ponder if I am {0}. How would my being {0} influence our conversation?",
        "Your question about me being {0} is intriguing. Why do you ask?"
    ],
    r'What (.*)': [
        "Asking 'what {0}' is a great start. What thoughts do you have on it?",
        "What {0} indeed. How does this question fit into your current thoughts?",
        "You're curious about {0}. Let's delve deeper into this."
    ],
    r'How (.*)': [
        "How indeed. What are your own thoughts on this?",
        "This question, 'how {0}', opens many possibilities. What are you feeling?",
        "Considering how {0} is an important step. Where does it lead you?"
    ],
    r'Because (.*)': [
        "Your reason, '{0}', is a significant insight. What more can we uncover about it?",
        "Understanding that {0} is the cause, what other factors come into play?",
        "You say {0}. Let's explore what underlying meanings this might have."
    ],
    r'(.*) sorry (.*)': [
        "Apologies can be powerful. What's prompting yours?",
        "You've mentioned feeling sorry about {0}. Let's understand these feelings together."
    ],
    r'Hello(.*)': [
        "Hello to you too. What's been on your mind today?",
        "Greetings. It seems like you're ready to talk. What would you like to start with?",
        "Hello there. How are you currently feeling?"
    ],
    r'I think (.*)': [
        "Thinking {0} is quite telling. Do you often feel this way?",
        "Your thoughts on {0} are worth exploring. What led you to this conclusion?"
    ],
    r'(.*) friend (.*)': [
        "Friends are important. Tell me more about yours.",
        "Your friendship with {0} sounds significant. What role do they play in your life?",
        "Discussing friends can be enlightening. What memories do you have with {0}?"
    ],
    r'Yes': [
        "Affirmation noted. Could you expand on that?",
        "You're certain. What further details can you provide?"
    ],
    r'(.*) computer(.*)': [
        "Discussing technology, are we? How does that make you feel?",
        "Your thoughts on computers are intriguing. Do they play a big role in your life?",
        "Computers and technology can evoke strong feelings. What's your stance?"
    ],
    r'Is it (.*)': [
        "You're wondering if it's {0}. What significance does the answer hold for you?",
        "The possibility of it being {0} seems to be on your mind. Why is that?"
    ],
    r'It is (.*)': [
        "You sound sure that it is {0}. How does knowing this affect you?",
        "Recognizing it as {0} can be impactful. What are your feelings on this?"
    ],
    r'Can you ([^\?]*)\??': [
        "You're asking if I can {0}. Why is this inquiry important to you?",
        "The question of my ability to {0} is interesting. What leads you to ponder this?"
    ],
    r'Can I ([^\?]*)\??': [
        "You're considering whether you can {0}. What makes you uncertain?",
        "The possibility of you doing {0} is on the table. How does it feel to think about that?"
    ],
    r'You are (.*)': [
        "Your perception of me as {0} is intriguing. How does this shape our dialogue?",
        "You view me as {0}. What does this reflect about your expectations?"
    ],
    r'You\'?re (.*)': [
        "Me being {0}, in your view, opens up many topics. Why do you see me this way?",
        "You describe me as {0}. Let's explore the meaning behind this."
    ],
    r'I don\'?t (.*)': [
        "Not doing {0} can be a significant choice. What's behind this decision?",
        "Your stance on not {0} is clear. What influences this?"
    ],
    r'I feel (.*)': [
        "Feeling {0} is a deeply personal experience. Can you share more?",
        "Your feelings of being {0} are important. What contributes to these feelings?"
    ],
    r'I have (.*)': [
        "Having {0} can affect one's perspective. How does it influence yours?",
        "You mention having {0}. Let's delve into how this impacts you."
    ],
    r'I would (.*)': [
        "You would {0}, under certain conditions. What are those conditions?",
        "Considering you would {0}, what factors make you say this?"
    ],
    r'Is there (.*)': [
        "Contemplating if there is {0} is a question worth examining. What are your thoughts?",
        "The existence of {0} is under question. Why do you bring this up?"
    ],
    r'My (.*)': [
        "Your {0} seems to hold significance. How do you feel about it?",
        "Discussing your {0} can provide insights. What's your relationship with it?"
    ],
    r'You (.*)': [
        "Our focus is on you, not me. But let's explore your thoughts further.",
        "Your statement about me doing {0} is interesting. Why do we focus on this?"
    ],
    r'Why (.*)': [
        "Seeking the reason for {0} can lead to deeper understanding. What are your initial thoughts?",
        "Your query about why {0} is compelling. Have you considered potential answers?"
    ],
    r'I want (.*)': [
        "Wanting {0} is a strong desire. What would fulfilling this desire mean to you?",
        "Your want for {0} is clear. How do you plan to achieve it?"
    ],
    r'(.*) mother(.*)': [
        "Your mother, and your relationship with her, seems to be on your mind. What feelings does this bring up?",
        "Discussing your mother can be emotional. What's your current perspective?"
    ],
    r'(.*) father(.*)': [
        "Fathers can play a complex role in our lives. How does this relate to you?",
        "Your father appears to be a significant figure. What dynamics are present?"
    ],
    r'(.*) child(.*)': [
        "Childhood experiences shape us in profound ways. What stands out to you from yours?",
        "Reflecting on being a child and those memories can be insightful. What do you remember most?"
    ],
    r'(.*)\?': [
        "Questions often reflect our innermost thoughts. What's behind yours?",
        "Inquiring about {0} suggests deep reflection. What answers are you seeking?"
    ],
    r'(.*)': [
        "Your statement, '{0}', brings many things to mind. Let's unpack this.",
        "Saying '{0}' reveals a lot. Can we explore this topic further?",
        "You mentioned '{0}'. This seems significant. Tell me more."
    ]
}

replace_dictionary = {
    "i'm" : 'I am',
    "i'd" : "I would",
    "i've" : "I have",
    "I'll" : "I will",
    "you've": "you have",
    "you'll": 'you will'
}


pronoun_dictionary = {
  "am"   : "are",
  "was"  : "were",
  "i"    : "you",
  "i would"  : "you would",
  "i have"  : "you have",
  "i will"  : "you will",
  "my"  : "your",
  "are"  : "am",
  "you have": "I have",
  "you will": "I will",
  "your"  : "my",
  "yours"  : "mine",
  "you"  : "me",
  "me"  : "you"
}

def transform_pronouns(statement):
    words = statement.split()
    transformed_words = [replace_dictionary.get(word,word) for word in words]
    transformed_words = [pronoun_dictionary.get(word,word) for word in transformed_words]
    return ' '.join(transformed_words)

def text_match_check(text):

    return re.match(r'([a-zA-z]+)', text, re.IGNORECASE)

def respond(statement):
    if ((Detector.is_gibberish(statement)) == True):
            response_template = "I didn't quite understand. Can you say that another way?"
            return response_template
    else:
        for pattern, responses_list in transformation_rules.items():
            match = re.search(pattern, statement, re.IGNORECASE)
            if match:
                response_template = random.choice(responses_list)
                try:
                    matched_part = match.group(1)
                    transformed_part = transform_pronouns(matched_part)
                    return response_template.format(transformed_part)
                except IndexError:
                    return response_template


def main():
    print("[eliza] Hi, I'm a psychotherapist. What is your name?")
    name = input().strip().capitalize()
    print(f"[eliza] Hi {name}. How can I help you today?")

    while True:
        statement = input().lower()
        if "quit" in statement:
            print("[eliza] Goodbye for now. Take care!")
            break
        
        response = respond(statement)
        print(f"=> [eliza] {response}")

if __name__ == "__main__":
    main()


# In[ ]:




