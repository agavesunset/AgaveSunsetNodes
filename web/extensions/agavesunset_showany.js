// file: web/extensions/agavesunset_showany.js
import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";

app.registerExtension({
  name: "AgaveSunset.ShowAny.SingleBox",
  beforeRegisterNodeDef(nodeType, nodeData, appInstance) {
    // NOTE: keep matching the old node type key for backward compatibility
    if (nodeData.name !== "Show_AgaveSunset") return;

    const normalizeText = (msgText) => {
      if (msgText == null) return "";

      // string: keep newlines
      if (typeof msgText === "string") return String(msgText);

      // array: handle char-array vs multi-line array
      if (Array.isArray(msgText)) {
        const flat = msgText.flat ? msgText.flat(Infinity) : [].concat(...msgText);
        const strs = flat.map((x) => String(x ?? ""));

        // char array: ["顶","你","个","肺"] -> "顶你个肺"
        if (strs.length > 0 && strs.every((s) => s.length === 1)) {
          return strs.join("");
        }

        // normal array: join by newline
        return strs.join("\n");
      }

      return String(msgText);
    };

    const ensureWidget = (node) => {
      let w = node.widgets?.find((w) => w.name === "__agavesunset_display__");
      if (!w) {
        if (Array.isArray(node.widgets)) {
          for (const old of [...node.widgets]) old.onRemove?.();
          node.widgets.length = 0;
        }

        w = ComfyWidgets["STRING"](
          node,
          "__agavesunset_display__",
          ["STRING", { multiline: true }],
          appInstance
        ).widget;

        const el = w.inputEl || w.element;
        if (el) {
          el.readOnly = true;
          el.style.pointerEvents = "auto";
          el.style.userSelect = "text";
          el.style.caretColor = "transparent";
          el.style.fontFamily = "inherit";
          el.style.lineHeight = "1.35";
          el.style.padding = "6px 8px";
          el.style.opacity = "0.95";
          el.spellcheck = false;
        }
      }
      return w;
    };

    const setText = (node, text) => {
      const w = ensureWidget(node);
      w.value = normalizeText(text);
      requestAnimationFrame(() => {
        const sz = node.computeSize();
        node.onResize?.(sz);
        appInstance.graph.setDirtyCanvas(true, false);
      });
    };

    const onExecuted = nodeType.prototype.onExecuted;
    nodeType.prototype.onExecuted = function (message) {
      onExecuted?.apply(this, arguments);
      setText(this, message?.text);
    };

    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      onNodeCreated?.apply(this, arguments);
      ensureWidget(this);
    };

    const configure = nodeType.prototype.configure;
    nodeType.prototype.configure = function () {
      const cfg = arguments[0];
      const ret = configure?.apply(this, arguments);
      const vals = cfg?.widgets_values;

      if (Array.isArray(vals) && vals.length > 0) {
        setText(this, vals);
      } else {
        ensureWidget(this);
      }
      return ret;
    };
  },
});
