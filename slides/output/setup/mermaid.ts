import { defineMermaidSetup } from "@slidev/types";

export default defineMermaidSetup(() => ({
  theme: "base",
  securityLevel: "strict",
  themeVariables: {
    fontFamily: "PingFang SC, Microsoft YaHei, sans-serif",
    fontSize: "25px",
    primaryColor: "#edf3fa",
    primaryTextColor: "#202833",
    primaryBorderColor: "#1a4a8a",
    lineColor: "#596675",
    secondaryColor: "#fcfcfa",
    tertiaryColor: "#edf3fa",
    noteBkgColor: "#edf3fa",
    noteTextColor: "#202833",
    actorBkg: "#edf3fa",
    actorBorder: "#1a4a8a",
    actorTextColor: "#202833",
  },
  flowchart: {
    htmlLabels: true,
    padding: 20,
    nodeSpacing: 40,
    rankSpacing: 40,
  },
  sequence: {
    actorFontSize: 24,
    messageFontSize: 23,
    noteFontSize: 23,
    mirrorActors: false,
  },
}));
