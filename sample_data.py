SAMPLE_CONVERSATIONS = [
    {
        "title": "Architect & Client Design Sync",
        "text": """
[10:30 AM] Sarah (Client Manager): Hi all, got the revised floor plans from Marcus. Thoughts?
[10:32 AM] Marcus (Architect): These reflect the layout changes we discussed Tuesday. The central atrium is now 20% larger.
[10:33 AM] Sarah (Client Manager): Love it. One issue though - client wants the revision presented by Friday EOD. That's tight.
[10:34 AM] Marcus (Architect): I can have the formal drawings done by Thursday if I drop everything else. But I need the approved material specs from procurement by Wednesday noon.
[10:35 AM] James (Procurement): Can do. I'll pin down the marble and lighting options with suppliers tomorrow.
[10:36 AM] Sarah (Client Manager): Great. Marcus, can you also update the 3D renderings? Client wants to see what it looks like in natural light.
[10:37 AM] Marcus (Architect): Yes, I'll add that. Sarah, once you present Friday, we should immediately schedule a follow-up with the structural engineer. We need sign-off on the atrium support.
[10:38 AM] Sarah (Client Manager): Good catch. I'll coordinate with Chen's team. Marcus - just to confirm - you can guarantee the drawings by Thursday evening?
[10:39 AM] Marcus (Architect): Thursday 5 PM. Set it in stone.
[10:40 AM] James (Procurement): I'll confirm specs by Tuesday EOD at the latest.
[10:41 AM] Sarah (Client Manager): Excellent. This is really coming together.
"""
    },
    {
        "title": "Contractor Group - Material Delay & Reassignment",
        "text": """
[2:15 PM] Mike (Site Lead): Team, we have a problem. The steel shipment is delayed 2 weeks. Was supposed to arrive Friday.
[2:16 PM] Dev (Foreman): That puts us behind the entire frame schedule. What's the new ETA?
[2:17 PM] Mike (Site Lead): October 3rd at earliest. The supplier had a production issue.
[2:18 PM] Lisa (Project Manager): We need to discuss contingencies. Can we re-sequence the work?
[2:19 PM] Dev (Foreman): We could shift the electrical rough-in earlier. That normally comes after framing, but we have inventory.
[2:20 PM] Mike (Site Lead): Good idea. Dev, can you pull together a revised schedule by tomorrow?
[2:21 PM] Dev (Foreman): On it. I'll also swap some crew. I'm moving Carlos from foundation details to assist Lisa with the electrical planning.
[2:22 PM] Carlos (Technician): Works for me.
[2:23 PM] Lisa (Project Manager): Thank you. Dev and I should sync up tomorrow at 9 AM to map out the new sequence.
[2:24 PM] Mike (Site Lead): Also - I'm escalating this to the vendor. We need them to confirm October 3rd or find us an alternative supplier by end of day tomorrow.
[2:25 PM] Dev (Foreman): Agreed. This delay could cost us. Lisa, I'll send you the revised timeline by 10 AM tomorrow so you can review before our sync.
[2:26 PM] Lisa (Project Manager): Perfect. Keep me posted.
"""
    },
    {
        "title": "Weekly Project Status Meeting - Q3 Closeout",
        "text": """
[3:00 PM] Janet (PM): Alright everyone, weekly standup. Let's start with blockers.
[3:02 PM] Tom (Engineering): We're blocked waiting on the API specs from the backend team. Need them ASAP to finish the integration layer.
[3:03 PM] Priya (Backend Lead): Yeah, sorry. We finalized specs yesterday. I'll send them to Tom by end of today. Tom, can you review and flag any issues by tomorrow morning?
[3:04 PM] Tom (Engineering): Absolutely.
[3:05 PM] Janet (PM): Great. Next - launch readiness. Priya?
[3:06 PM] Priya (Backend Lead): We're 90% done with the payment processing module. One edge case on refunds that's still being tested. I'll have it fully certified by Thursday.
[3:07 PM] Janet (PM): Excellent. That's been the biggest risk. Priya, once you certify, we need a sign-off from legal and finance. Can you coordinate that Thursday afternoon?
[3:08 PM] Priya (Backend Lead): I'll set up a call and walk them through it.
[3:09 PM] Marc (QA): On my end, I've found 3 medium-severity bugs this week. All logged. I'll prioritize them. Two are in authentication - those go to Tom.
[3:10 PM] Tom (Engineering): Got it. I'll pull those into my sprint.
[3:11 PM] Janet (PM): Marc, can you send me a summary of all open issues ranked by severity? I need to present the risk assessment to the steering committee Friday morning.
[3:12 PM] Marc (QA): I'll have it to you by Thursday EOD.
[3:13 PM] Janet (PM): One more thing - product launch date. We're still targeting October 15th?
[3:14 PM] Priya (Backend Lead): I'm confident on that. Assuming the refund edge case is closed by Thursday, we're good.
[3:15 PM] Janet (PM): That's still pending your testing, Priya. Everyone else good?
[3:16 PM] Tom (Engineering): Frontend is on track.
[3:17 PM] Marc (QA): Assuming no new blockers, we can be ready for launch testing by Sept 25th.
[3:18 PM] Janet (PM): Perfect. I'm taking this to leadership as green light pending Priya's refund cert by Thursday. Priya - that's your critical gate. You good?
[3:19 PM] Priya (Backend Lead): Thursday, refund testing complete, sign-off coordination scheduled.
[3:20 PM] Janet (PM): Excellent. That's all for today. Let's reconvene same time next week.
"""
    }
]

def get_sample_by_index(index: int) -> str:
    """Get a sample conversation by index (0, 1, or 2)."""
    if 0 <= index < len(SAMPLE_CONVERSATIONS):
        return SAMPLE_CONVERSATIONS[index]['text']
    return SAMPLE_CONVERSATIONS[0]['text']

def get_all_samples() -> list:
    """Get all sample conversations."""
    return SAMPLE_CONVERSATIONS
