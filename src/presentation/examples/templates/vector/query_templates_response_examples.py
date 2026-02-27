QUERY_TEMPLATES_RESPONSE_EXAMPLES = {
	200: {
		"description": "Success",
		"content": {
			"application/json": {
				"examples": {
					"Normal": {
						"value": [
							{
								"id": "0c9d97dc-dd58-4425-aff3-edc95b15c15a",
								"vector": [0.1, 0.2, 0.3],
								"payload": {
									"upload_date": "2024-01-01T12:00:00",
									"text": "Text associated to the point.",
								},
							},
							{
								"id": "0c9d97dc-dd58-4425-aff3-edc95b15c15b",
								"vector": [0.1, 0.2, 0.6],
								"payload": {
									"upload_date": "2024-01-01T12:00:00",
									"text": "Text associated to the point.",
								},
							},
						]
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
					"Generic error": {"value": {"message": "An error occurred while query for templates"}},
				}
			}
		},
	},
}
