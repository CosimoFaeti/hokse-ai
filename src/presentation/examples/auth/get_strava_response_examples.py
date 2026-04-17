GET_STRAVA_RESPONSE_EXAMPLES = {
	302: {
		"description": "Redirect to Strava consent screen.",
		"content": {"application/json": {"example": {"detail": "Redirecting to Strava..."}}},
	},
	500: {
		"description": "Internal server error.",
		"content": {"application/json": {"example": {"detail": "Internal server error."}}},
	},
}
