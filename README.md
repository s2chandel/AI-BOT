# GETTING STARTED
Run flask HTTP server

>Run application.py
# API ENDPOINT
>'Content-Type: application/json'

```POST /chat``` --- For Rule Based BOT

```POST /talk``` --- For AI_BOT

>'https://recipebot.azurewebsites.net/talk'


## Request Body :

```json
{
    "user_id":251991, "user_message":"hi"

}
```
## Response from bot: 

```json
{
    "message": "Hi Sharon",
}
```
***
***

# Sample conversation between Rule_Based_Bot and client

> Similar as the RuleBased Bot

# Sample conversation between AI_Bot and client

>REQUEST
```json
{
    "user_id":251991, "user_message":"hey"
}
```  

RESPONSE
```json
{
    "message": "Hello! Sharon"
}
```  


>REQUEST: 
```json
{
    "user_id":251991, "user_message":"can you tell me Should I eat carbs before exercise"
}
```

RESPONSE:
```json
{
    "message": "The simple answer, no. For normal exercise intensity, LCHF dieting is perfectly safe and will also be beneficial for weight loss. However, for long distance runners and people exercising at moderate to high intensity for over 90 minutes, carbs may be needed." **FAQs**
}
```


>REQUEST:
```json
{
    "user_id":251991, "user_message":"you are amazing"

}
```

RESPONSE:
```
{
    "message": "Thanks Sharon"
}
```


>REQUEST:
```json
{
    "user_id":251991, "user_message":"tell me some headlines"
}
```

RESPONSE:
```json
{
    {
    "message": {
    "status": "ok",
    "totalResults": 18,
    "articles": [
    {
    "source": {
    "id": "abc-news-au",
    "name": "ABC News (AU)"
    },
    "author": "Roscoe Whalan And Daniel Keane",
    "title": "Fifty years for a reply? 'It's worse than the British mail service', jokes letter-in-bottle author",
    "description": "Paul Gilmore feared bad news when his phone blew up with messages this week. But it was merely the end of a journey he began 50 years ago with a letter in a bottle.",
    "url": "https://www.abc.net.au/news/2019-07-19/message-in-a-bottle-sender-delighted-by-discovery-50-years-later/11323400",
    "urlToImage": "https://www.abc.net.au/news/image/11323646-16x9-700x394.jpg",
    "publishedAt": "2019-07-18T15:53:00Z",
    "content": "Updated \r\nJuly 19, 2019 02:08:35\r\nPaul Gilmore has not taken many cruises during his 63 years, but his current holiday has taken an unexpected detour into his past, and the media spotlight.\r\nKey points:\r\n<ul><li>In 1969, a 13-year-old English migrant dropped … [+4944 chars]"
    }
        **News Api**
}
```


>REQUEST:
```
{
"user_id":251991, "user_message":"tell me something about yourself ?"
}
```

RESPONSE:
```json
{
"message": "Hello! I’m your virtual AI assistant developed at Diabetes Digital Media"
}       
```


>REQUEST:
```
{
    "user_id":251991, "user_message":"best exercise routine"
}
```

RESPONSE:
```json
{
    "message": "Sorry I dont have a response for that.\n This is what I found on google:\nhttps://www.shape.com/fitness/workouts/your-best-exercise-routine-right-now"
}               **FAQ not found search google**  
```


>REQUEST:
```json
{
    "user_id":251991, "user_message":"anything for lunch"
}
```

RESPONSE:
```json
{
"message": "Selected Category: Lunch\nNumber of Recipes found: 48\n1: Scrambled Eggs on Pea Pancakes (v)\n2: Morning Refreshment (v)\n3: Oaty Fruit Starter (v)\n4: Greek Yoghurt Bowl (v)\n5: Aubergine and Cauliflower Biryani (v)\n6: Creamy Vegetable Curry with Low Carb Naan Bread (v)\n7: Tamarind Vegetable Stir Fry (v)\n
}
```


>REQUEST:
```json
{
    "user_id":251991, "user_message":"you're not good"
}
```

RESPONSE:
```json
{
    "message": "Are you unsatisfied with my service?\n Yes/No"
}
```


>REQUEST:
```json
{
    "user_id":251991, "user_message":"yes"
}
```

RESPONSE:
{
```json
    "message": "Sorry! If I wasn’t up to your expectations"
}
```


>REQUEST:
```json
{
    "user_id":251991, "user_message":"suggest me some recipe"
}
```

RESPONSE:
```json
{
    "message": "Hmm, What are you looking for in particular Sharon?"
}
```


>REQUEST:
```json
{
    "user_id":251991, "user_message":"suggest me some random recipes"
}
```

RESPONSE:
{
```json
{
    "message": "Selected Dietary type: Pescetarian\nNumber of Recipes found: 7\n1: Creamy Garlic Prawn Linguine\n2: Pesto & Pumpkin Seed Courgetti (v)\n3: Keto Courgette Lasagne (v)\n4: Tiramisu Mousse (v)\n5: Raw Broccoli and Kale Pesto (v)\n6: Vegetable & Lentil Ragu with Courgetti (v)\n7: Creamy Garlic & Basil Tofu with Asparagus & Courgetti (v)\nPlease select the Recipe number to recieve cooking instructions."
}
```


>REQUEST:
```json
{
"user_id":251991, "user_message":"3"
}
```

RESPONSE:
{
```json
{
    "message": "\nCooking Instructions:  Preheat oven to 200°C/180°C fan (390°F/350°F fan).  For the lasagne sauce, heat ½ of the oil in a non-stick pan over a medium heat. Add the onions and garlic and cook until tender.  Add the mushrooms, aubergine and frozen peppers and cook until slightly tender. Add the passata and mustard powder and season with salt and pepper.  Bring the mixture to the boil, then reduce to a low heat and leave to simmer for 20 minutes.  In the meantime prepare the white sauce by combining the ricotta, sour cream and egg in a bowl and season with salt and pepper.  In a large casserole dish spread a thin layer of the lasagne sauce. Top with a layer of the courgette slices, white sauce mixture and a sprinkle of cheddar. Repeat this process until all ingredients are used.  Bake in the oven for 20-25 minutes, or until the courgette is tender.  Remove from the oven and serve with the rocket, drizzled in the olive oil.  "
}
```


>REQUEST:
```json
{
    "user_id":251991, "user_message":"great"
}
```

RESPONSE:
{
```json
{
    "message": "I just try"
}
```

***
.
.
.
.

