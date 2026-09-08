/**
 * Mermaid init for MkDocs (or similar) publish paths.
 * Markdown flowcharts must still embed classDef blocks for non-MkDocs viewers.
 */
(function () {
  function boot() {
    if (typeof mermaid === "undefined") return;
    mermaid.initialize({
      startOnLoad: true,
      theme: "base",
      themeVariables: {
        primaryColor: "#cfe2f3",
        primaryTextColor: "#0d47a1",
        primaryBorderColor: "#1565c0",
        lineColor: "#546e7a",
        secondaryColor: "#b2dfdb",
        tertiaryColor: "#c8e6c9",
      },
      flowchart: { curve: "basis" },
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
