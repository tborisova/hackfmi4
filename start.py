import json
null = None
b = {"side": 0,
"background": [55,155,255],
"buttons":
	{"join":
		{"type": "default",
		"dimensions": (255, 50),
		"pos": (200, 300),
		"text": "Join",
		"text_color": [0, 0, 0],
		"text_font": [null, 100]
		},
	 "create":
		{"type": "default",
		"dimensions": (255, 50),
		"pos": (200, 380),
		"text": "Create",
		"text_color": [0, 0, 0],
		"text_font": [null, 100]
		}
	},
"text_boxes":
	{"title":
		{"dimensions": (300, 100),
		"pos": (200, 100),
		"text": "Challange Accepted",
		"background": None,
		"text_font": [r"data/fonts/font.tff", 100],
		"text_color": [0, 0, 0]
		}
},
"input_boxes":
	{}
}
z = {"side": 1,
"background": [55,155,255],
"buttons":
"default", (255, 50), (555, 300), "Maze Runner", None, (0, 0, 0), (None, 100)
	{"maze":
		{"type": "default",
		"dimensions": (255, 50),
		"pos": (200, 300),
		"text": "Join",
		"text_color": [0, 0, 0],
		"text_font": [null, 100]
		},
	 "create":
		{"type": "default",
		"dimensions": (255, 50),
		"pos": (200, 380),
		"text": "Create",
		"text_color": [0, 0, 0],
		"text_font": [null, 100]
		}
	},
"text_boxes":
	{"title":
		{"dimensions": (300, 100),
		"pos": (200, 100),
		"text": "Challange Accepted",
		"background": None,
		"text_font": [r"data/fonts/font.tff", 100],
		"text_color": [0, 0, 0]
		}
},
"input_boxes":
	{}
}
a = open("start.l", "w")
a.write(json.dumps(b))
a.close()