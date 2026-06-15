import { Select } from "../../components/ui/Select.jsx";

export function ModelSelector({ models, value, onChange, compact = false }) {
  return (
    <Select
      className={compact ? "w-[220px]" : "w-full"}
      value={value || ""}
      onChange={(event) => onChange(event.target.value)}
    >
      <option value="">Conversation default</option>
      {models.map((model) => (
        <option key={model.model_id} value={model.model_id}>
          {model.display_name} - {model.capabilities_json?.label || model.provider}
        </option>
      ))}
    </Select>
  );
}

