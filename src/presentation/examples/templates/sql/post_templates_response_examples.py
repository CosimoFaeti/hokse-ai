POST_TEMPLATES_RESPONSE_EXAMPLES = {
	201: {
		"description": "Success",
		"content": {
			"application/json": {
				"examples": {
					"Normal": {
						"value": {
							"id": "0c9d97dc-dd58-4425-aff3-edc95b15c15a",
							"description": "This is the description of the template",
						}
					},
				}
			}
		},
	},
	500: {
		"description": "Internal Server Error",
		"content": {
			"application/json": {
				"examples": {
					"Generic error": {"value": {"message": "An error occurred while adding the template"}},
				}
			}
		},
	},
}
