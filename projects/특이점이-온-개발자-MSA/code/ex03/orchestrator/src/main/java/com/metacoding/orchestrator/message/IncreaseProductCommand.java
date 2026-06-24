package com.metacoding.orchestrator.message;

public record IncreaseProductCommand(int orderId, int productId, int quantity, long price) {}
