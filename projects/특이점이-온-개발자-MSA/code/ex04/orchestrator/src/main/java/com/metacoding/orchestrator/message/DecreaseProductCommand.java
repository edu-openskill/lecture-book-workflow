package com.metacoding.orchestrator.message;

public record DecreaseProductCommand(int orderId, int productId, int quantity, long price) {}
