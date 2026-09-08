# Developer documentation

| Page | Content |
|------|---------|
| [architecture.md](architecture.md) | System structure, tick loop, non-goals |
| [contributing.md](contributing.md) | Add algorithm / scenario / metric |
| [config_and_presets.md](config_and_presets.md) | Experiment config resolution |
| [testing.md](testing.md) | Test layout and expectations |

## Mermaid palette

Every flowchart embeds these `classDef` lines so diagrams render outside MkDocs:

```text
classDef ui fill:#cfe2f3,stroke:#1565c0,color:#0d47a1
classDef wiring fill:#b2dfdb,stroke:#00796b,color:#004d40
classDef domain fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
classDef shared fill:#e1bee7,stroke:#7b1fa2,color:#4a148c
classDef transport fill:#ffe0b2,stroke:#ef6c00,color:#e65100
classDef question fill:#fff9c4,stroke:#f9a825,color:#5d4037
classDef start fill:#eceff1,stroke:#546e7a,color:#263238
```

Legend footer (identical on every flowchart page):

`Legend: blue = UI, teal = wiring/config, green = domain models, purple = shared core, orange = transport, yellow = decision, grey = start/end.`

Site helper: [../javascripts/mermaid-init.js](../javascripts/mermaid-init.js).
