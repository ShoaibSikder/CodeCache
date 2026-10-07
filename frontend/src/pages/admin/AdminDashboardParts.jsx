import { Loader2, Pencil, Trash2 } from "lucide-react";

export function StatusBadge({ status }) {
  return (
    <span
      className={`text-xs px-2 py-0.5 rounded-full font-medium ${
        status === "active"
          ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400"
          : status === "draft"
            ? "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400"
            : "bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400"
      }`}
    >
      {status || "active"}
    </span>
  );
}

export function ActionBtns({ onEdit, onDelete, disabled = false, deleting = false }) {
  return (
    <div className="flex gap-1">
      <button
        onClick={onEdit}
        disabled={disabled}
        className="p-1.5 rounded-md hover:bg-muted transition-colors"
        title="Edit"
      >
        <Pencil className="h-3.5 w-3.5" />
      </button>
      <button
        onClick={onDelete}
        disabled={disabled || deleting}
        className="p-1.5 rounded-md hover:bg-red-100 hover:text-red-600 transition-colors"
        title="Delete"
      >
        {deleting ? (
          <Loader2 className="h-3.5 w-3.5 animate-spin" />
        ) : (
          <Trash2 className="h-3.5 w-3.5" />
        )}
      </button>
    </div>
  );
}
