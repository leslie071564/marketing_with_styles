politeness_config = {
    'keywords': ['polite/formal (フォーマル)', 
                 'casual (カジュアル)'],
    'output_keys': ['formal', 'casual'],
    'allow_content_change': False,
    'few_shots': [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "1. 初めまして、ライカです。\n2. 今日は京都の観光地について紹介します。"
                }
            ]
            },
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": "{\n  \"formal\": [\n    \"初めまして、ライカと申します。\",\n    \"本日は京都の観光地についてご紹介いたします。\"\n  ],\n  \"casual\": [\n    \"初めまして、ライカです。\",\n    \"今日は京都の観光地について紹介しますね。\" \n  ]\n}"
                }
            ]
            }   # add more if necessary.
            ]
}

rationality_config = {
    'keywords': ['rational (理性的)', 
                 'emotional (感性的).'],
    'output_keys': ['rational', 'emotional'],
    'allow_content_change': True,
    'few_shots':[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "1. 初めまして、ライカです。\n2. 今日は京都の観光地について紹介します。"
                }
            ]
            },
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": "{\n  \"rational\": [\n    \"はじめに自己紹介をさせていただきます。私の名前はライカです。\",\n    \"本日は、京都の主要な観光スポットについて詳しく説明いたします。\"\n  ],\n  \"emotional\": [\n    \"初めまして！私、ライカと申します！\",\n    \"今日は、美しい京都の観光地を一緒に探検しましょうね！\" \n  ]\n}"
                }
            ]
            }   # add more if necessary.
        ]
}