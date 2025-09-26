// file: web/extensions/agavesunset_showany.js
import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";

app.registerExtension({
  name: "AgaveSunset.ShowAny.SingleBox",
  beforeRegisterNodeDef(nodeType, nodeData, appInstance) {
    if (nodeData.name !== "Show_AgaveSunset") return;

    // 统一成“横向一段文本”
    const normalizeText = (msgText) => {
      const squash = (s) => String(s ?? "").replace(/\r\n|\r|\n/g, " "); // 换行→空格
      if (typeof msgText === "string") return squash(msgText);
      if (Array.isArray(msgText)) {
        const flat = msgText.flat ? msgText.flat(Infinity) : [].concat(...msgText);
        return flat.map(squash).join(" "); // 数组用空格拼接
      }
      return squash(msgText);
    };

    // 确保只有“一个只读多行框”
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
          el.readOnly = true;                 // 只读
          el.style.pointerEvents = "auto";    // 允许选择/复制
          el.style.userSelect = "text";
          el.style.caretColor = "transparent"; // 不显示光标（看起来不可编辑）
          el.style.fontFamily =
            "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace";
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

    // 执行后从后端 ui.text 接收
    const onExecuted = nodeType.prototype.onExecuted;
    nodeType.prototype.onExecuted = function (message) {
      onExecuted?.apply(this, arguments);
      setText(this, message?.text);
    };

    // 创建节点时先放一个空框
    const onNodeCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      onNodeCreated?.apply(this, arguments);
      ensureWidget(this);
    };

    // 载入工作流时，若有历史 widgets_values，合并为一段横向文本
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
