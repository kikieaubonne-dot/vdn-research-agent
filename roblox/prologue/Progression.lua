-- Original PROPOSED laboratory module; NOT executed in Roblox Studio.
-- Caller must validate scene ownership and player/event authority on the server.
-- No RemoteEvent, asset mutation, publication, network or automatic ending.
local Progression = {}
local transitions = {
  ["home-postit"] = { event = "POSTIT_READ", nextState = "home-maelle" },
  ["home-maelle"] = { event = "MAELLE_LEAVES", nextState = "follow-maelle" },
  ["follow-maelle"] = { event = "MAELLE_LOST", nextState = "search-maelle" },
  ["search-maelle"] = { event = "SILHOUETTE_ENCOUNTERED", nextState = "escape" },
  ["escape"] = { event = "SAFE_PLACE_REACHED", nextState = "call-police" },
  ["call-police"] = { event = "REPORT_MADE", nextState = "investigator" },
  ["investigator"] = { event = "INVESTIGATION_INTRO_COMPLETE", nextState = "ending-decision-required" },
}
function Progression.new()
  return { state = "home-postit", sequence = 0, seen = {} }
end
function Progression.advance(current, event, eventId)
  assert(type(eventId) == "string" and #eventId > 0 and #eventId <= 64, "bounded event ID required")
  if current.seen[eventId] then
    assert(current.seen[eventId] == event, "idempotency conflict")
    return current, false
  end
  local transition = transitions[current.state]
  assert(transition and transition.event == event, "unexpected event or undecided ending")
  current.seen[eventId] = event
  current.state = transition.nextState
  current.sequence = current.sequence + 1
  return current, true
end
return Progression
