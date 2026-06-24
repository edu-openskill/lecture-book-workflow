package com.metacoding.orchestrator.message;

public record ProductDecreasedEvent(int orderId, int productId, int quantity, boolean isSuccess) {}
