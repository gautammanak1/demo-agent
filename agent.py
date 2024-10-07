from pydantic import Field
from uagents import Agent, Context, Protocol, Model
from ai_engine import UAgentResponse, UAgentResponseType
import requests
from datetime import datetime

job_protocol = Protocol(name="job_protocol")

class JobRequest(Model):
    job_description: str = Field(description="Give details of job you are looking for")

async def get_job_details(job_role, rapidapi_key):
    url = "https://linkedin-data-api.p.rapidapi.com/search-jobs-v2"
    querystring = {
        "keywords": job_role,
        "locationId": "92000000",  # This ID corresponds to the United States
        "datePosted": "anyTime",
        "sort": "mostRelevant"
    }
    headers = {
        'x-rapidapi-key': rapidapi_key,
        'x-rapidapi-host': "linkedin-data-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

rapidapi_key = "f8ebddb48dmsh99308dca542ff6dp16a906jsn6618329dda68"

@job_protocol.on_message(model=JobRequest, replies={UAgentResponse})
async def load_job(ctx: Context, sender: str, msg: JobRequest):
    ctx.logger.info(f"Received job request: {msg.job_description}")
    
    try:
        details = await get_job_details(msg.job_description, rapidapi_key)
        ctx.logger.info(f"Job details for {msg.job_description}: {details}")

        # Check if details contain error
        if 'error' in details:
            message = f"Error fetching job details: {details['message']}"
        else:
            message = ""
            for detail in details.get('data', []):
                ctx.logger.info(detail)
                job_url = detail.get('url')
                job_title = detail.get('title')
                company_name = detail.get('company', {}).get('name')
                location = detail.get('location')
                post_date = detail.get('postDate')

                message += (f"<a href='{job_url}'>{job_title}</a>\n"
                            f"Company: {company_name}\n"
                            f"Location: {location}\n"
                            f"Posted: {post_date}\n\n")
    except Exception as e:
        ctx.logger.error(f"An error occurred while fetching job details: {e}")
        message = f"An unexpected error occurred: {e}"

    await ctx.send(sender, UAgentResponse(message=message, type=UAgentResponseType.FINAL))

agent = Agent()
agent.include(job_protocol, publish_manifest=True)
