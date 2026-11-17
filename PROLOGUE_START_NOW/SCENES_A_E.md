# A→E — référence et déclencheurs proposés

Source : Bible r3, chapitres r2, missionV10/V11. Le logiciel de progression est un témoin ; les vraies observations de scène restent à brancher.

## A — Maison familiale

Statut narratif : CONFIRMED

- home-postit : Lire le message des parents. Rôle : Léo ; événement témoin : POSTIT_READ → home-maelle
- home-maelle : Suivre Maëlle. Rôle : Léo ; événement témoin : MAELLE_LEAVES → follow-maelle
## B — Poursuite de Maëlle

Statut narratif : CONFIRMED

- follow-maelle : Suivre Maëlle ; Shift seulement si nécessaire. Rôle : Léo ; événement témoin : MAELLE_LOST → search-maelle
## C — Recherche et confrontation

Statut narratif : CONFIRMED

- search-maelle : Retrouve Maëlle. Rôle : Léo ; événement témoin : SILHOUETTE_ENCOUNTERED → escape
- escape : Échapper à la menace. Rôle : Léo ; événement témoin : SAFE_PLACE_REACHED → call-police
## D — Appel à la police

Statut narratif : CONFIRMED

- call-police : Signaler la disparition. Rôle : Léo ; événement témoin : REPORT_MADE → investigator
## E — Enquêteur

Statut narratif : CONFIRMED

- investigator : Rechercher les indices ; apprentissage approfondi proposé. Rôle : Policier ; événement témoin : INVESTIGATION_INTRO_COMPLETE → ending-decision-required
## F — Fin à décider

Statut narratif : UNKNOWN

- ending-decision-required : Attendre une décision sur la fin. Rôle : UNKNOWN ; événement témoin : None → None

Contraintes confirmées :
- Parents already absent; Léo watches Maëlle.
- First pursuit: only Shift sprint if necessary; no forced advanced movement tutorial.
- Police investigator becomes playable in phase E.
- Ending F remains UNKNOWN; preserve interactivity.
